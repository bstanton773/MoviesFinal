from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import Movies
from app.forms import SearchForm



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
    return render_template('search.html', form=form, movies=movies)