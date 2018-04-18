from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import Movies
from app.forms import SearchForm
from flask_login import current_user



@app.route('/')
@app.route('/index')
def index():
    movies = Movies.query.all()
    return render_template('index.html', title='Home', movies = movies)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    if form.search.data is not None:
        movies = Movies.query.filter(Movies.title.like('%' + form.search.data + '%')).all()
    else:
        movies = Movies.query.limit(10)
    return render_template('search.html', form=form, movies=movies, title='Search')

@app.route('/review/<int:movieId>')
def review(movieId):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    movie = Movies.query.filter_by(movieId = movieId).first()
    return render_template('review.html', movie = movie, title='Review')