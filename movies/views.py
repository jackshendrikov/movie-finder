import difflib
import pandas as pd

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.forms import UserRegisterForm
from users.models import Watchlist
from users.models import Review

movies = pd.read_csv('movies.csv')
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
    return render(request, 'registration/register.html', {'form': form})


@login_required
def watchlist(request):
    movie = request.POST.get('movie')
    user_title_watchlist = list([x.movie for x in Watchlist.objects.filter(author=request.user)])

    if request.method == 'POST':
        if movie[:6] != "delete":
            if movie not in user_title_watchlist:
                add_movie = Watchlist(movie=movie, author=request.user)
                messages.success(request, f'{movie} successfully added to your watchlist!')
                add_movie.save()
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.info(request, f'{movie} was already in your watchlist!')
                return redirect(request.META['HTTP_REFERER'])
        else:
            delete_movie = Watchlist.objects.filter(movie=movie[6:], author=request.user)
            messages.error(request, f'{movie[6:]} has been deleted from your watchlist!')
            delete_movie.delete()
            return redirect('watchlist')

    df_user_watchlist = movies.set_index('title').loc[user_title_watchlist].reset_index(inplace=False)
    user_watchlist = df_user_watchlist.values.tolist()[::-1]
    print(user_watchlist)

    page = request.GET.get('page', 1)
    paginator = Paginator(user_watchlist, 15)

    try:
        user_watchlist = paginator.page(page)
    except PageNotAnInteger:
        user_watchlist = paginator.page(1)
    except EmptyPage:
        user_watchlist = paginator.page(paginator.num_pages)

    return render(request, 'watchlist.html', {'userWatchlist': user_watchlist})


def main_page(request):
    return render(request, 'main-page.html', {'movieList': dfList})


# def all_movies(request):
#     return render(request, 'all.html', {'dfList': dfList})
#
#
# def all_series(request):
#     dfSeries = movies[movies['type'] == 'Series'].values.tolist()
#     return render(request, 'series.html', {'movieList': dfSeries})
#
#
def top_movies(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(dfTopList, 15)

    try:
        movie_items = paginator.page(page)
    except PageNotAnInteger:
        movie_items = paginator.page(1)
    except EmptyPage:
        movie_items = paginator.page(paginator.num_pages)

    return render(request, 'top100.html', {'movieItems': movie_items})


def advanced_search(request):
    df_advance = movies.copy()
    all_cast = list(set([j for sub in list(movies['cast'].str[2:-2].str.replace("'", "").str.replace('"', '')
                                           .str.split(', ')) for j in sub]))

    global paginator
    page = request.GET.get('page', 1)

    if request.method == 'GET' and (request.GET.get('getYear') is not None or request.GET.get('getRate') is not None) \
            and request.GET.get('page') is None:
        get_rating = request.GET.get('getRate')
        get_year = request.GET.get('getYear')
        get_cast = request.GET.get('getCast')
        get_keywords = request.GET.get('getKeywords')
        get_genre = request.GET.get('getGenre')

        sorting = request.GET.get('sorting')
        get_cast = difflib.get_close_matches(get_cast, all_cast)

        if len(get_cast) > 0: get_cast = get_cast[0]
        else: get_cast = ''

        if get_genre == 'All': get_genre = ''
        if not get_year: get_year = 0
        if not get_rating: get_rating = 0.0

        if sorting == 'byYear':
            dfSelect = df_advance[(df_advance['rating'] >= float(get_rating)) & (df_advance['year'] >= int(get_year)) &
                                  (df_advance['genre'].str.contains(get_genre, na=False)) &
                                  (df_advance['cast'].str.contains(get_cast, na=False)) &
                                  (df_advance['keywords'].str.contains(get_keywords, na=False))].sort_values(by='year', ascending=False)
        elif sorting == 'byVotes':
            dfSelect = df_advance[(df_advance['rating'] >= float(get_rating)) & (df_advance['year'] >= int(get_year)) &
                                  (df_advance['genre'].str.contains(get_genre, na=False)) &
                                  (df_advance['cast'].str.contains(get_cast, na=False)) &
                                  (df_advance['keywords'].str.contains(get_keywords, na=False))].sort_values(by='votes', ascending=False)
        else:
            dfSelect = df_advance[(df_advance['rating'] >= float(get_rating)) & (df_advance['year'] >= int(get_year)) &
                                  (df_advance['genre'].str.contains(get_genre, na=False)) &
                                  (df_advance['cast'].str.contains(get_cast, na=False)) &
                                  (df_advance['keywords'].str.contains(get_keywords, na=False))].sort_values(by='rating', ascending=False)

        dfSelect = dfSelect.values.tolist()
        if get_genre == '': get_genre = 'All'
        if get_cast == '': get_cast = 'All'
        if get_keywords == '': get_keywords = 'Any'

        if sorting == 'byYear': sorting = 'By Year'
        elif sorting == 'byVotes': sorting = 'By Votes'
        else: sorting = 'By Rating'

        paginator = Paginator(dfSelect, 15)

        try:
            movie_items = paginator.page(page)
        except PageNotAnInteger:
            movie_items = paginator.page(1)
        except EmptyPage:
            movie_items = paginator.page(paginator.num_pages)

        return render(request, 'advanced_search.html', {'getRate': get_rating, 'getYear': get_year,
                                                        'getGenre': get_genre, 'getCast': get_cast,
                                                        'getKeywords': get_keywords, 'sorting': sorting,
                                                        'movieItems': movie_items})
    elif request.method == 'GET' and \
            (request.GET.get('getYear') is None or request.GET.get('getRate') is None) and \
            request.GET.get('page') is not None:
        try:
            movie_items = paginator.page(page)
        except EmptyPage:
            movie_items = paginator.page(paginator.num_pages)

        return render(request, 'advanced_search.html', {'movieItems': movie_items})
    else:
        return render(request, 'advanced_search.html')


# def genre_page(request):
#     genre_type = request.GET.get('typeGenre', 'False')
#     if genre_type == 'Netflix':
#         df1 = movies.copy()
#         df1 = df1[df1['netflix'].notna()]
#         dfTopNet = df1.sort_values(by='rating', ascending=False)
#         genre = dfTopNet.values.tolist()
#         return render(request, 'genre.html', {'movieList': genre, 'genre_type': genre_type})
#
#     genre = []
#     for i in range(0, len(movies)):
#         if genre_type in movies["genre"][i]:
#             genre.append(movies.iloc[i].values.tolist())
#
#     dfByGenre = pd.DataFrame(genre, columns=['imdb_id', 'title', 'rating', 'link', 'votes', 'genre', 'cast', 'runtime',
#                                              'type', 'netflix', 'plot', 'keywords', 'year', 'poster'])
#     dfTopGenre = dfByGenre.sort_values(by='rating', ascending=False)
#     genre = dfTopGenre.values.tolist()
#
#     return render(request, 'genre.html', {'movieList': genre, 'genre_type': genre_type})
#

def show_intro(request):
    youtube = request.POST.get('intro', 'False')
    title = request.POST.get('title', 'False')

    if youtube != 'False' and title != 'False':
        return render(request, "intro.html", {'youtube': "https://www.youtube.com/watch?v=" + youtube, 'title': title})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def result_page(request):
    movie = request.POST.get('movie', False)
    intro = request.POST.get('intro', False)
    msg = request.POST.get('msg', False)
    if movie:
        search = movies[movies['title'] == movie]

        imdb_id = search['imdb_id'].to_string(index=False).strip()
        title = search['title'].to_string(index=False).strip()
        rating = int(float(search['rating'].to_string(index=False).strip()) * 10)
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
        year = search['year'].to_string(index=False).strip()
        if intro == 'noIntro':
            youtube = 'None'
            intro = 'Played'
        else:
            youtube = search['youtube'].to_string(index=False).strip()
            intro = 'None'

        if msg:
            messages.success(request, msg)

        reviews = Review.objects.filter(movie=title)
        reviews_rate = False
        if reviews:
            reviews_rate = [(range(int(review.rating)), range(int(10-review.rating))) for review in reviews]

        full_result = {'movie': movie, 'imdb_id': imdb_id, 'title': title, 'rating': rating, 'link': link,
                       'votes': votes, 'genres': genres, 'cast': cast, 'runtime': runtime, 'mtype': mType,
                       'netflix': netflix, 'plot': plot, 'poster': poster, 'genres_split': genres_split,
                       'year': year, 'youtube': youtube, 'cast_list': cast_list, 'reviews': reviews,
                       'reviews_rate': reviews_rate, 'intro': intro}

        return render(request, "result.html", full_result)
    else:
        messages.error(request, f'Error occurred while we\'re trying to show you info about the movie!')
        return redirect('/')
