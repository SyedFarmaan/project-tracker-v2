# 📊 Project Tracker

A Flask-based web app to help you keep track of personal or team projects, built as part of a backend learning journey with SQLAlchemy, Flask-WTF, and HTML templates.



## 🚀 Features

- Add new projects with title and description
- View list of added projects with timestamp
- Form validation with Flask-WTF
- SQLite database integration using SQLAlchemy
- Styled frontend with Bootstrap



## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-WTF, SQLAlchemy
- **Database:** SQLite (via SQLAlchemy ORM)
- **Frontend:** HTML, Bootstrap 5, CSS
- **Version Control:** Git + GitHub



## 📸 Screenshots

> _(Add these later)_
- Home page
- Add project form
- Project list view



## 🔧 Setup Instructions

1. **Clone the repo**
   (CMD)
   git clone https://github.com/SyedFarmaan/project-tracker.git
   cd project-tracker

2. **Create virtual environment**
   (CMD)
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate

3. **Install dependencies**
    pip install -r requirements.txt

4. **Run the flask app**
    flask run

**folder sructure**
   project-tracker/
│
├── app.py               # Flask entry point
├── forms.py             # WTForms for project input
├── data.db              # SQLite DB
├── requirements.txt     # Dependencies
├── static/
│   └── styles.css       # Custom styles
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   └── projects.html
└── .gitignore           # Ignore venv,__pycache__



