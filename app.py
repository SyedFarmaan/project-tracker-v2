from flask import Flask,render_template,redirect,url_for,flash,request,session
from werkzeug.security import generate_password_hash, check_password_hash 
from forms import ContactForm,ProjectForm,DeleteForm,RegisterForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from functools import wraps

 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#login required decorator 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

#--------------------------------------------------------------------
#Admin required decorator 
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function




# database models


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Contact {self.name}>"
    
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)



app.secret_key = "your_secret_key_here"  # You can generate a random one for production

#flask routesss(public)

@app.route('/')
def home():
    return render_template("index.html",name="Farmaan")

@app.route("/about")
def about():
    return render_template("about.html",name="Farmaan")

#Contact routes(protected)

@app.route("/contact",methods=["GET","POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data

        #Save to database
        new_msg = Contact(name=name, message=message)
        db.session.add(new_msg)
        db.session.commit()

        # flashing back to the user
        flash("Your message was saved successfully!")
        return redirect(url_for("contact"))
    return render_template("contact.html",form=form)#the first form refers to the
    #html form and the next form is the object of the flaskwtf forms

@app.route("/messages")
@login_required
def messages():
    all_msgs = Contact.query.all()
    return render_template("messages.html", messages=all_msgs)

@app.route("/delete/<int:msg_id>", methods=["POST"])
@login_required
def delete_message(msg_id):
    msg_to_delete = Contact.query.get_or_404(msg_id)
    db.session.delete(msg_to_delete)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect("/messages")


#Project Routes(protected)

@app.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    form = ProjectForm()
    delete_form = DeleteForm()

    search_query = request.args.get("search", "").strip()

    if search_query:
        all_projects = Project.query.filter(Project.title.ilike(f"%{search_query}%")) \
            .order_by(Project.created_at.desc()).all()
    else:
        all_projects = Project.query.order_by(Project.created_at.desc()).all()

    if form.validate_on_submit():
        new_proj = Project(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(new_proj)
        db.session.commit()
        flash("Project added!", "success")
        return redirect(url_for("projects"))

    return render_template("projects.html", form=form, delete_form=delete_form, projects=all_projects, search_query=search_query)


@app.route("/projects/delete/<int:proj_id>", methods=["POST"])
@login_required
def delete_project(proj_id):
    proj_to_delete = Project.query.get_or_404(proj_id)
    db.session.delete(proj_to_delete)
    db.session.commit()
    flash("Project deleted!", "success")
    return redirect("/projects")

#routes for login and registration
#last changed register route

#Auth Routes(public)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken. Please choose a different one.", "danger")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully. You can now log in!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

#admin route

@app.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    if not session.get("is_admin"):
        flash("You are not authorized to view this page.", "danger")
        return redirect(url_for("home"))
    
    users = User.query.all()
    return render_template("admin.html", users=users)

@app.route("/admin/promote/<int:user_id>", methods=["POST"])
@login_required
def promote_user(user_id):
    if not session.get("is_admin"):
        flash("Admin access required.", "danger")
        return redirect(url_for("admin_dashboard"))

    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("User is already an admin.", "info")
    else:
        user.is_admin = True
        db.session.commit()
        flash(f"{user.username} has been promoted to admin.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not session.get("is_admin"):
        flash("Admin access required.", "danger")
        return redirect(url_for("admin_dashboard"))

    user = User.query.get_or_404(user_id)

    if user.id == session["user_id"]:
        flash("You cannot delete your own account!", "warning")
        return redirect(url_for("admin_dashboard"))

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} has been deleted.", "success")
    return redirect(url_for("admin_dashboard"))





#MAIN

if __name__ =='__main__':
    app.run(debug=True)