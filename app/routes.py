from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import Movies, Reviews
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

@app.route('/watchlist')
def watchlist():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    movies_in_watchlist = Reviews.query.filter_by(user_id = current_user.id, watchlist=1).join(
        Movies, Reviews.movie_id == Movies.movieId).add_columns(
        Movies.title, Movies.genres, Movies.year, Movies.movieId).all()
    return render_template('watchlist.html', title='My Watchlist', movies = movies_in_watchlist)

@app.route('/addToWatchlist/<int:movieId>/<string:from_page>')
def addToWatchlist(movieId, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    watch = Reviews(user_id = current_user.id, movie_id = movieId, watchlist=1)
    db.session.add(watch)
    db.session.commit()
    return redirect(url_for('search'))

@app.route('/removeFromWatchlist/<int:movieId>/<string:from_page>')
def removeFromWatchlist(movieId, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    watch = Reviews.query.filter_by(user_id = current_user.id, movie_id = movieId, watchlist=1).first()
    db.session.delete(watch)
    db.session.commit()
    if from_page == 'watchlist':
        return redirect(url_for('watchlist'))
    else:
        return redirect(url_for('search'))