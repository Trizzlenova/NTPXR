from flask import render_template, url_for, flash, redirect, jsonify
from ntpxr import app
from ntpxr.find_and_update_movie_data import *

@app.route('/')
@app.route('/home')
def home():
  movies = Movie.query.all()
  return render_template('main.html', movies=movies)

@app.route("/movies/api", methods=["GET"])
def get_movie():
    movie = Movie.query.all()
    result = movies_schema.dump(movie)
    return jsonify(result.data)

@app.route("/genre/api", methods=["GET"])
def get_genre():
  genre = Genre.query.all()
  result = genre_schema.dump(genre)
  return jsonify(result.data)
