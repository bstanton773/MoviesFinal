from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import Movies, Reviews, User
from app.forms import SearchForm, ReviewForm
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

@app.route('/review/<int:movieId>', methods=['GET','POST'])
def review(movieId):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    form = ReviewForm()
    if form.validate_on_submit():
        if len(form.comment.data) == 0:
            rating = Reviews(user_id = current_user.id, movie_id = movieId, rating=form.rating.data)
            db.session.add(rating)
            db.session.commit()
        else:
            rating_comment = Reviews(user_id=current_user.id, movie_id=movieId, rating=form.rating.data, comment=form.comment.data)
            db.session.add(rating_comment)
            db.session.commit()
    movie = Movies.query.filter_by(movieId = movieId).first()
    comments = Reviews.query.filter_by(movie_id = movieId).join(
        Movies, Reviews.movie_id == Movies.movieId).join(
        User, Reviews.user_id == User.id).add_columns(
        Movies.title, Movies.movieId, Reviews.comment, User.username).all()
    return render_template('review.html', movie = movie, title='Review', form=form, comments=comments)

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

@app.route('/myreviews')
def myreviews():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    my_reviews = Reviews.query.filter_by(user_id = current_user.id).join(
        Movies, Reviews.movie_id == Movies.movieId).add_columns(
        Movies.title, Movies.genres, Movies.year, Movies.movieId, Reviews.rating, Reviews.comment).all()
    print(my_reviews)
    return render_template('myreviews.html', title='My Watchlist', reviews = my_reviews)