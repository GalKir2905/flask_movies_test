from flask import render_template, redirect, url_for
from . import app, db
from .models import Review, Movie


@app.route('/')
def index():
    film = Movie.query.order_by(Movie.id.desc).all()
    return render_template('index.html',
                           movies=film)
