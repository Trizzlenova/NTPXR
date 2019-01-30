# change name to find_and_update_movie_data.py
from ntpxr import app, db
from ntpxr.models import Movie, Genre, movies_schema, genre_schema
import requests
from bs4 import BeautifulSoup
import re
from random import randint
from ntpxr.config import key

def randomizer(arr):
  return arr[randint(0, len(arr))]

# =====================================
# grab the data
movie_url = requests.get('https://www.netflix.com/browse/genre/34399?so=az')

soup = BeautifulSoup(movie_url.text, 'html.parser')

data = []
main = soup.find('div', {'id': 'appMountPoint'})

for div in main.findAll('div'):
  for li in div.findAll('li'):
    for span in li.findAll('span', {'class': "nm-collections-title-name"}):
      data.append(span.text)

data = list(set(data))[:0]
# =====================================


# db.drop_all()
db.create_all()

# =====================================
# replacing spaces with '+' for url input
def replace(title):
  return re.sub(r'\s+', '+', title)

# converting a string to a list
def str_to_list(str):
  return str.split(', ')

def genre_validator(cat):
  genre_list = str_to_list(cat)
  for g in genre_list:
    if db.session.query(Genre.id).filter_by(category=g).scalar() is None:
      add_genre_to_db = Genre(category = g)
      db.session.add(add_genre_to_db)
      db.session.commit()
      # print(f'adding {g} to Genre database: {Genre.query.all()}')


# put in new folder inside the app directory.
# loading the database
for film in data:
  # if Movie['title'] exists:
  if db.session.query(Movie.id).filter_by(title=film).scalar() is not None:
    print(f'{film} exists in the database')
    continue
  else:
    film_to_db = requests.get(f'http://www.omdbapi.com/?t={replace(film)}&apikey={key}')
    try:
      movie_db_info = film_to_db.json()
      genre_validator(movie_db_info['Genre'])
      adding_new_movie_to_db = Movie(title=movie_db_info['Title'], image=movie_db_info['Poster'], genre=movie_db_info['Genre'], year_released=movie_db_info['Year'], plot=movie_db_info['Plot'], actors=movie_db_info['Actors'], director=movie_db_info['Director'], rating=movie_db_info['imdbRating'], type=movie_db_info['Type'], production=movie_db_info['Production'])
      db.session.add(adding_new_movie_to_db)
      print(f"adding {movie_db_info['Title']} to Movie db")
      genre_list = str_to_list(movie_db_info['Genre'])
      # print(genre_list)
      for g in genre_list:
        genre_id = db.session.query(Genre.id).filter_by(category=g).scalar()
        grab_genre_model = Genre.query.get(genre_id)
        movie_id = db.session.query(Movie.id).filter_by(title=movie_db_info['Title']).scalar()
        grab_movie_model = Movie.query.get(movie_id)
        grab_genre_model.movie_list.append(grab_movie_model)
        # print(f"adding {movie_db_info['Title']} to {grab_genre_model}")
    except:
      pass

    db.session.commit()

# =====================================

# with open('comedy.py', 'w') as c:
#   c.write(str(data))
