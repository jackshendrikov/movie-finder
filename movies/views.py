import difflib
import requests
import pandas as pd

from bs4 import BeautifulSoup
from django.contrib import messages
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm

movies = pd.read_csv('../movies.csv')
pd.set_option('display.max_colwidth', None)

dfList = movies.values.tolist()
dfTop = movies.sort_values(by='rating', ascending=False)[0:100]
dfTopList = dfTop.values.tolist()


def register(request):
    if request.user.is_authenticated:
        return redirect('main_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Created Account for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def main_page(request):
    return render(request, 'main_page.html', {'movieList': dfList})


def all_movies(request):
    return render(request, 'all.html', {'dfList': dfList})


def all_series(request):
    dfSeries = movies[movies['type'] == 'Series'].values.tolist()
    return render(request, 'series.html', {'movieList': dfSeries})


def top_movies(request):
    return render(request, 'top100.html', {'movieList': dfTopList})


def advanced_search(request):
    df_advance = movies.copy()
    all_cast = list(set([j for sub in list(movies['cast'].str[2:-2].str.replace("'", "").str.replace('"', '')
                                           .str.split(', ')) for j in sub]))

    if request.method == 'GET':
        get_rating = request.GET.get('getRate')
        get_year = request.GET.get('getYear')
        get_cast = request.GET.get('getCast')
        get_keywords = request.GET.get('getKeywords')
        get_genre = request.GET.get('getGenre')

        sorting = request.GET.get('inlineDefaultRadios')
        get_cast = difflib.get_close_matches(get_cast, all_cast)

        if len(get_cast) > 0: get_cast = get_cast[0]
        else: get_cast = ''

        if get_genre == 'All': get_genre = ''
        if not get_year: get_year = 0
        if not get_rating: get_rating = 0.0

        if sorting == 'byyear':
            dfSelect = df_advance[(df_advance['rating'] >= float(get_rating)) & (df_advance['year'] >= int(get_year)) &
                                  (df_advance['genre'].str.contains(get_genre, na=False)) &
                                  (df_advance['cast'].str.contains(get_cast, na=False)) &
                                  (df_advance['keywords'].str.contains(get_keywords, na=False))].sort_values(by='year',
                                                                                                             ascending=False)
        else:
            dfSelect = df_advance[(df_advance['rating'] >= float(get_rating)) & (df_advance['year'] >= int(get_year)) &
                                  (df_advance['genre'].str.contains(get_cast, na=False)) &
                                  (df_advance['cast'].str.contains(get_cast, na=False)) &
                                  (df_advance['keywords'].str.contains(get_keywords, na=False))].sort_values(by='rating',
                                                                                                             ascending=False)
        dfSelect = dfSelect.values.tolist()

        if get_genre == '': get_genre = 'All'
        if get_cast == '': get_cast = 'All'
        if get_keywords == '': get_keywords = 'Any'
        if sorting == 'byyear': sorting = 'By Year'
        else: sorting = 'By Rating'

        return render(request, 'advanced_search.html', {'movieList': dfSelect, 'movieLen': len(dfSelect),
                                                        'getRate': get_rating, 'getYear': get_year,
                                                        'getGenre': get_genre, 'getCast': get_cast,
                                                        'getKeywords': get_keywords, 'sorting': sorting})
    else:
        return render(request, 'advanced_search.html')


def genre_page(request):
    genre_type = request.GET.get('typeGenre', 'False')
    if genre_type == 'Netflix':
        df1 = movies.copy()
        df1 = df1[df1['netflix'].notna()]
        dfTopNet = df1.sort_values(by='rating', ascending=False)
        genre = dfTopNet.values.tolist()
        return render(request, 'genre.html', {'movieList': genre, 'genre_type': genre_type})

    genre = []
    for i in range(0, len(movies)):
        if genre_type in movies["genre"][i]:
            genre.append(movies.iloc[i].values.tolist())

    dfByGenre = pd.DataFrame(genre, columns=['imdb_id', 'title', 'rating', 'link', 'votes', 'genre', 'cast', 'runtime',
                                             'type', 'netflix', 'plot', 'keywords', 'year', 'poster'])
    dfTopGenre = dfByGenre.sort_values(by='rating', ascending=False)
    genre = dfTopGenre.values.tolist()

    return render(request, 'genre.html', {'movieList': genre, 'genre_type': genre_type})


def result_page(request):
    movie = request.POST.get('movie', 'False')
    search = movies[movies['title'] == movie]

    # params
    imdb_id = search['imdb_id'].to_string(index=False).strip()
    title = search['title'].to_string(index=False).strip()
    rating = search['rating'].to_string(index=False).strip()
    link = search['link'].to_string(index=False).strip()
    votes = search['votes'].to_string(index=False).strip()
    genres = search['genre'].to_string(index=False).strip()
    genres_split = genres.split(',')
    cast = search['cast'].to_string(index=False).strip()
    cast_list = cast[2:-2].replace("'", "").split(',')
    runtime = search['runtime'].to_string(index=False).strip()
    mType = search['type'].to_string(index=False).strip()
    netflix = search['netflix'].to_string(index=False).strip()
    plot = search['plot'].to_string(index=False).strip()
    poster = search['poster'].to_string(index=False).strip()

    full_result = {'movie': movie, 'imdb_id': imdb_id, 'title': title, 'rating': rating, 'link': link,
                   'votes': votes, 'genres': genres, 'cast': cast, 'runtime': runtime, 'mtype': mType,
                   'netflix': netflix, 'plot': plot, 'poster': poster, 'genres_split': genres_split,
                   'cast_list': cast_list}

    if movies[movies['imdb_id'] == imdb_id]['netflix'].to_string(index=False).strip() != "NaN":
        back = True
        soup = BeautifulSoup(requests.get(netflix).text, "html.parser")
        raw = soup.find("div", {'class': 'hero-image hero-image-desktop'})
        try:
            background = raw.get('style')[35:-2]
            logo = soup.find("img", {'class': 'logo'}).get('src')
            return render(request, "result.html", {'movie': movie, 'imdb_id': imdb_id, 'title': title, 'rating': rating,
                                                   'link': link, 'votes': votes, 'genres': genres, 'cast': cast,
                                                   'runtime': runtime, 'mtype': mType, 'netflix': netflix,
                                                   'plot': plot, 'poster': poster, 'logo': logo,
                                                   'background': background, 'back': back, 'genres_split': genres_split,
                                                   'cast_list': cast_list})
        except:
            return render(request, "result.html", full_result)
    return render(request, "result.html", full_result)
