from flask import render_template, redirect, url_for
from . import app, db
from .models import Movie, Review, User
from .forms import ReviewForm, AddMovieForm, LoginForm, RegistretionForm
from flask_login import login_user, logout_user, login_required, current_user, login_manager
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    film = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           films=film)

@app.route('/movie/<int:id>',  methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    form = ReviewForm(score=5)
    if movie.review:
        score = round(sum(x.score for x in movie.review) / len(movie.review), 2)
    else:
        score = 0
    if form.validate_on_submit():
        rewiew = Review()
        rewiew.name = form.name.data
        rewiew.text = form.text.data
        rewiew.score = form.score.data
        rewiew.movie_id = movie.id
        db.session.add(rewiew)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html',
                           nice_score=score,
                           form=form,
                           movie=movie)


@app.route('/add_movie')
# @login_required
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.name = form.title.data
        movie.description = form.description.data
        file_name = secure_filename(form.image.file.filename)
        # form.image.file.save(f"/z/Program/FAUST/flask_movie_test/app/static/images/{file_name}") ## PATH!!!!
        # movie.image = form.image.data
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('add_movie', id=movie.id))
    return render_template('add_movie.html', form=form)


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
