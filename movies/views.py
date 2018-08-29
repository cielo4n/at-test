from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Movie, Genre, Torrent
from datetime import datetime


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
            pass

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
