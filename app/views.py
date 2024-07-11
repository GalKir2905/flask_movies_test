from flask import render_template
from . import app
from . models import Movie
from pathlib import Path
from .forms import ReviewForm
from .models import Movie, Review

BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'

@app.route('/')
def index():
    film = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',movies=film)

@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewForm(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html',
                           movie=movie,
                           avg_score=avg_score,
                           form=form)