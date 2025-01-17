from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', back_populates='movie')

    def __repr__(self):
        return f'Фильм {self.id}: ({self.title})'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', ondelete="CASCADE"))
    movie = db.relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f'Отзыв {self.id}: ({self.title[:20]}...)'


class Roles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_name = db.Column(db.String(255), nullable=False, default="Owner")
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User', back_populates='roles')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    roles = db.relationship('Roles', back_populates='user')

    def __repr__(self):
        return f"User {self.name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)