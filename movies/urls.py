from django.urls import include, path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.main_page, name="main-page"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    path('specials/', TemplateView.as_view(template_name='specials.html'), name='specials'),
    path('genres/', TemplateView.as_view(template_name='genres.html'), name='genres'),
    path('watchlist/', views.watchlist, name="watchlist"),
    path('genre/', views.genre, name='genre'),
    path('popular/', views.popular, name='popular'),

    # path('all', views.all_movies, name='all'),
    path('series/', views.all_series, name='series'),
    path('top/', views.top_movies, name='top100'),
    path('netflix/', views.netflix, name='netflix'),

    path('search/', views.movie_search, name='movie-search'),
    path('advsearch/', views.advanced_search, name='advanced-search'),

    path('intro/', views.show_intro, name='show-intro'),
    path('movie-info/<str:movie_id>/', views.result_page, name='result'),
]
