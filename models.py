from flask_sqlalchemy import SQL_Alchemy # type: ignore

db = SQL_Alchemy()

class User(db.Model):
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Task(db.Model):
    id = db.column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'))
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))