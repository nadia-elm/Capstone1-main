from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cocktail_name = db.Column(db.String(80), nullable=False)
    cocktail_id = db.Column(db.Integer, nullable=False)
    cocktail_image = db.Column(db.String(255), nullable=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)


def connect_db(app):
    db.app = app
    db.init_app(app)
