from flask import render_template, redirect, url_for
from . import app, db
import os
from pathlib import Path
from .forms import ReviewForm, RegistretionForm, LoginForm, MovieForm
from .models import Movie, Review, User
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.utils import secure_filename

BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'

@app.route('/')
def index():
    film = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html', movies=film)

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

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        file_image_name = form.image.data
        file_name = secure_filename(file_image_name.filename)
        movie.image = file_name
        file_image_name.save(f"{UPLOAD_FOLDER}/{file_name}", )
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_movie.html', form=form)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    review = Review.query.all()
    movie = Movie.query.all()
    return render_template('reviews.html',
                           review=review,
                           movie=movie)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistretionForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
    return render_template('login.html',
                           form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/delete_review/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_reviews(id):
    Review.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('reviews'))

@app.route('/all_movies', methods=['GET', 'POST'])
def all_movies():
    movie = Movie.query.all()
    return render_template('delete_films.html',
                           movie=movie)


@app.route('/delete_movie/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_movie(id):
    movie_images = Movie.query.get(id)
    os.remove(f"{UPLOAD_FOLDER}/{movie_images.image}")
    Movie.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/search/<string:title>', methods=['GET', 'POST'])
# def search(title):
#     movie_search = Movie.query.filter_by(title=title).first_or_404()
#     return redirect(url_for('movie', id=movie_search.id))
