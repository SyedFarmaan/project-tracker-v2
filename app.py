from flask import Flask,render_template,redirect,url_for,flash,request
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
 

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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



app.secret_key = "your_secret_key_here"  # You can generate a random one for production


@app.route('/')
def home():
    return render_template("index.html",name="Farmaan")

@app.route("/about")
def about():
    return render_template("about.html",name="Farmaan")

#Sqldb creationn 

@app.route("/contact",methods=["GET","POST"])
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
def messages():
    all_msgs = Contact.query.all()
    return render_template("messages.html", messages=all_msgs)

@app.route("/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    msg_to_delete = Contact.query.get_or_404(msg_id)
    db.session.delete(msg_to_delete)
    db.session.commit()
    flash("Message deleted successfully!", "success")
    return redirect("/messages")

@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        new_proj = Project(title=title, description=desc)
        db.session.add(new_proj)
        db.session.commit()
        flash("Project added!", "success")
        return redirect("/projects")
    
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("projects.html", projects=all_projects)




if __name__ =='__main__':
    app.run(debug=True)