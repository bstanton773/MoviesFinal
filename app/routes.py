from app import app, db
from flask import render_template, redirect, url_for, flash
from app.models import Movies



@app.route('/')
@app.route('/index')
def index():
    movies = Movies.query.all()
    return render_template('index.html', title='Home', movies = movies)