from flask import render_template
from . import app
from .models import Movie


@app.route('/')
def index():
    film = Movie.query.order_by(Movie.id.desc).all()
    return render_template('index.html',
                           movies=film)
