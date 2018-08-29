from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Movie, Genre, Torrent
from datetime import datetime
import json
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
def yts_movie_list_save(request):
    params = dict()
    page = request.GET.get('page')
    limit = request.GET.get('limit')

    if page:
        params['page'] = int(page)
    if limit:
        params['limit'] = int(limit)

    yts_url = 'https://yts.am/api/v2/list_movies.json'
    response = requests.get(yts_url, params=params)
    res_dict = response.json()
    data = res_dict.get('data')
    movie_list = data.get('movies')
    time_format = '%Y-%m-%d %H:%M:%S'

    # 영화 저장
    for ml in movie_list:
        if Movie.objects.filter(id=ml.get('id')):
            continue

        movie = Movie(
            id=ml.get('id'),
            url=ml.get('url'),
            imdb_code=ml.get('imdb_code'),
            title=ml.get('title'),
            title_english=ml.get('title_english'),
            title_long=ml.get('title_long'),
            slug=ml.get('slug'),
            year=ml.get('year'),
            rating=ml.get('rating'),
            runtime=ml.get('runtime'),
            summary=ml.get('summary'),
            description_full=ml.get('description_full'),
            synopsis=ml.get('synopsis'),
            yt_trailer_code=ml.get('yt_trailer_code'),
            language=ml.get('language'),
            mpa_rating=ml.get('mpa_rating'),
            background_image=ml.get('background_image'),
            background_image_original=ml.get('background_image_original'),
            small_cover_image=ml.get('small_cover_image'),
            medium_cover_image=ml.get('medium_cover_image'),
            large_cover_image=ml.get('large_cover_image'),
            state=ml.get('state'),
            date_uploaded_unix=ml.get('date_uploaded_unix'),
        )
        movie.date_uploaded = datetime.strptime(ml.get('date_uploaded'), time_format)
        movie.save()

        # 장르 저장
        genre_list = ml.get('genres')
        for gl in genre_list:
            if Genre.objects.filter(name__iexact=gl):
                gen = Genre.objects.get(name__iexact=gl)
            else:
                gen = Genre(name=gl)
                gen.save()
            movie.genres.add(gen)

        # 토렌트 저장
        torrent_list = ml.get('torrents')
        for tl in torrent_list:
            torrent = Torrent(
                url=tl.get('url'),
                hash=tl.get('hash'),
                quality=tl.get('quality'),
                seeds=tl.get('seeds'),
                peers=tl.get('peers'),
                size=tl.get('size'),
                size_bytes=tl.get('size_bytes'),
                date_uploaded_unix=tl.get('date_uploaded_unix'),
            )
            torrent.date_uploaded = datetime.strptime(tl.get('date_uploaded'), time_format)
            torrent.movie = movie
            torrent.save()

    return HttpResponse(response.text, content_type='application/json')


def movie_list_view(request):
    time_format = '%Y-%m-%d %H:%M:%S'

    if request.method == 'GET':
        res = dict()

        movie_list = Movie.objects.filter()

        limit = int(request.GET.get('limit', 20))
        if limit < 1 or limit > 50:
            limit = 20

        page = int(request.GET.get('page', 1))

        quality = request.GET.get('quality', 'All')
        minimum_rating = int(request.GET.get('minimum_rating', 0))

        if 0 <= minimum_rating <= 9:
            movie_list = movie_list.filter(rating__gte=minimum_rating)

        query_term = request.GET.get('query_term', 0)
        if query_term:
            movie_list = movie_list.filter(Q(title__icontains=query_term) | Q(title_english__icontains=query_term)
                                           | Q(title_long__icontains=query_term) | Q(imdb_code__icontains=query_term))

        genre = request.GET.get('genre', 'All')
        if genre != 'All':
            movie_list = movie_list.filter(genres__name__iexact=genre)

        order_by = request.GET.get('order_by', 'desc')
        if order_by == 'asc':
            order = ''
        else:
            order = '-'

        sort_by = request.GET.get('sort_by', 'date_added')
        if sort_by in ['title', 'year', 'rating']:
            movie_list = movie_list.order_by(order+sort_by)
        else:
            movie_list = movie_list.order_by(order+'date_uploaded')

        paginator = Paginator(movie_list, limit)
        page_obj = paginator.page(page)
        movie_list = page_obj.object_list

        # 응답 만들기
        res['status'] = 'ok'
        res['status_message'] = 'Query was successful'
        res['data'] = {
            'movie_count': paginator.count,
            'limit': limit,
            'page_number': page,
        }
        res['movies'] = list()

        for ml in movie_list:
            movie_dict = model_to_dict(ml)
            movie_dict['genres'] = [gen.name for gen in ml.genres.all()]
            movie_dict['date_uploaded'] = datetime.strftime(ml.date_uploaded, time_format)

            movie_dict['torrents'] = list()
            torrent_list = Torrent.objects.filter(movie=ml)
            if quality in ['720p', '1080p', '3D']:
                torrent_list = torrent_list.filter(quality=quality)

            for tl in torrent_list:
                torrent_dict = model_to_dict(tl)
                torrent_dict['date_uploaded'] = datetime.strftime(tl.date_uploaded, time_format)
                del torrent_dict['id']
                del torrent_dict['movie']
                movie_dict['torrents'].append(torrent_dict)

            res['movies'].append(movie_dict)

        return HttpResponse(json.dumps(res), content_type='application/json')

    elif request.method == 'POST':
        pass
    return HttpResponse({}, content_type='application/json')
