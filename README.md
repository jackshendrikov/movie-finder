<h1 align="center">Movie Finder</h1>

<p align="center">
  <img src="img/movie-genres.png" alt="Welcome Logo" width="800">
</p>


This Django project is designed to search for movies, and in the future to receive recommendations through the neural network.

The user can search for movies by advanced search (rating, actors, keywords, years) or simply by title. In the "Specials" category you can see a list of Netflix movies, TOP-100 movies or a list of popular series. There is also a category of new popular movies.

When you go to some pages of movies or TV series (for example, "The Witcher"), you can see a short intro to the TV series or movie (videos are pulled from YouTube).

A registered user can add reviews to movies, rate them and add movies to the watchlist.

### 📝 &nbsp;Requirements

- **Django** (`v3.1+`)
- **Python** (`v3.8+`)
- **pandas** (`v1.3.0+`)
- **Gunicorn** (`v19.6+`)
- **django-heroku** (`v0.3.1`)
- **django-extensions** (`v3.0.5`)
- **dj_database_url** (`v0.5.0`)
- **psycopg2** (`v2.8.6`)
- **python-decouple** (`v3.4`)
- **whitenoise** (`v5.2.0`)

### ✨ &nbsp;Features

|                                        FEATURE                                       | IMPLEMENTATION |
|:------------------------------------------------------------------------------------:|:--------------:|
| __Search movies by title__                                                               | ✔️              |
| __Advanced movie search__ (_by rating, genre, keywords, year, cast_)                       | ✔️              |
| __Add/update/delete reviews__                                                            | ✔️              |
| __Add/remove movies from the watchlist__                                                 | ✔️              |
| __View all reviews__ (_admin only_)                                                        | ✔️              |
| __Browse a list of popular movies__                                                      | ✔️              |
| __Browse the list of movies by selected genre__                                          | ✔️              |
| __Browse the list of movies by special categories__ (_TOP-100, Netflix movies, TV series_) | ✔️              |
| __Excellent UI + optimization for smartphones__                                          | ✔️              |
| __Ability to login/register__                                                            | ✔️              |
| __Add recommendations based on the neural network__                                      | ❌              |
| __Add rewards to users__                                                                 | ❌              |
| __Add a chat__                                                                           | ❌              |

### 📷 App Screenshots

Advanced Search         |  User Profile | Movies List (Grid View)       |  Movies List (List View)
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
<img src="img/movie-adv-search.png" title="Advanced Search" width="100%"> |<img src="img/movie-user.png" title="User Profile" width="100%">|<img src="img/movie-grid.png" title="Movies List (Grid View) " width="100%"> |<img src="img/movie-list.png" title="Movies List (List View)" width="100%">


Movie Page         |  Movie Intro  | Genres Page      |  Special Categories
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
<img src="img/movie-page.png" title="Movie Page " width="100%"> |<img src="img/movie-intro.png" title="Movie Intro" width="100%">|<img src="img/movie-genres.png" title="Genres Page" width="100%"> |<img src="img/movie-specials.png" title="Special Categories" width="100%">


Review Form         |  Movie Reviews  | My Reviews       |  My Watchlist
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
<img src="img/movie-review.png" title="Review Form " width="100%"> |<img src="img/movie-reviews.png" title="Movie Reviews" width="100%">|<img src="img/movie-my-reviews.png" title="My Reviews" width="100%"> |<img src="img/movie-watchlist.png" title="My Watchlist" width="100%">


### 💡 &nbsp;Additional Info

Movies are loaded to the database from the `movies.csv` file with help of `movies_load.py`, this script reads the whole table and if some data from the table is not in our database, it adds them there.

To add data to the `movies.csv` format table, another script is used - `movie_parser.py`. There you will also need a OMDB API key, you can get it here - [omdbapi.com](http://www.omdbapi.com/).

🔥 To deploy the project on **Heroku**, read [this wonderful article](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment).

## 📫 &nbsp;Get in touch

<p align="center">
<a href="https://www.linkedin.com/in/yevhenii-shendrikov-6795291b8/"><img src="https://img.shields.io/badge/-Jack%20Shendrikov-0077B5?style=flat&logo=Linkedin&logoColor=white"/></a>
<a href="mailto:jackshendrikov@gmail.com"><img src="https://img.shields.io/badge/-Jack%20Shendrikov-D14836?style=flat&logo=Gmail&logoColor=white"/></a>
<a href="https://www.facebook.com/jack.shendrikov"><img src="https://img.shields.io/badge/-Jack%20Shendrikov-1877F2?style=flat&logo=Facebook&logoColor=white"/></a>
<a href="https://t.me/jackshen"><img src="https://img.shields.io/badge/-@jackshen-0088cc?style=flat&logo=Telegram&logoColor=white"/></a>
</p>