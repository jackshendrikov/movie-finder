from django.urls import path
from . import views

urlpatterns = [
    # Main Movie Logic
    path('', views.main_page, name="main-page"),
    # path('register', views.register, name="register"),
    # path('all', views.all_movies, name='all'),
    # path('allseries', views.all_series, name='series'),
    # path('top', views.top_movies, name='top100'),
    path('advsearch', views.advanced_search, name='advanced-search'),
    # path('genre', views.genre_page, name='genre-page'),
    # path('result', views.result_page, name='result'),
    # path('watchlist/', views.watchlist, name="watchlist"),
]
