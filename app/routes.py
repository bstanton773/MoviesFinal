from app import app, db
from flask import render_template, redirect, url_for, flash



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')