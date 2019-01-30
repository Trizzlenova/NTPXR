from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import Schema, fields
from ntpxr import db, ma

movie_genre_association_table = db.Table('movie_genre_association_table',
  db.metadata,
  db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
  db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
  )

class Genre(db.Model):
  __tablename__ = 'genre'
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(50), nullable=False)
  movie_list = db.relationship('Movie', secondary=movie_genre_association_table,
                            backref=db.backref('genres', lazy='dynamic'))

  def __repr__(self):
    return f'Genre({self.category})'


class Movie(db.Model):
  __tablename__ = 'movies'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False)
  image = db.Column(db.String(250), nullable=False)
  genre = db.Column(db.String(50), nullable=False)
  year_released = db.Column(db.String(20), nullable=False)
  plot = db.Column(db.String(250), nullable=False)
  actors = db.Column(db.String(50), nullable=False)
  director = db.Column(db.String(50), nullable=False)
  rating = db.Column(db.String(10), nullable=False)
  type = db.Column(db.String(10), nullable=False)
  production = db.Column(db.String(50), nullable=False)

  def __repr__(self):
    return f"Movie('{self.id}', '{self.title}', '{self.image}', '{self.genre}', '{self.year_released}', '{self.plot}', '{self.actors}', '{self.director}', '{self.rating}', '{self.type}', '{self.production}')"

class MovieSchema(ma.Schema):
  id = fields.Str(dump_only=False)
  title = fields.Str()
  class Meta:
    type_='movies'
    fields = ('title', 'image', 'genre', 'year_released', 'plot', 'actors', 'director', 'rating', 'type', 'production')

class GenreSchema(ma.Schema):
  id = fields.Str(load_only=True)
  category = fields.Str()
  movie_list = fields.Nested(MovieSchema, only=['title', 'image', 'genre', 'year_released', 'plot', 'actors', 'director', 'rating', 'type', 'production'], many=True)

  class Meta:
    fields = ('category', 'movie_list')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
genre = Genre()
genre_schema = GenreSchema(many=True)

