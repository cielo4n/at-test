from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# POST : title, year, rating, genres, summary 만 필수입력
class Movie(models.Model):
    url = models.CharField(max_length=500, blank=True, default='')
    imdb_code = models.CharField(max_length=200, blank=True, default='')
    title = models.CharField(max_length=500)
    title_english = models.CharField(max_length=500, blank=True, default='')
    title_long = models.CharField(max_length=500, blank=True, default='')
    slug = models.SlugField(max_length=500, blank=True, default='')
    year = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    runtime = models.IntegerField(default=0)

    genres = models.ManyToManyField(Genre)

    summary = models.TextField()
    description_full = models.TextField(blank=True, default='')
    synopsis = models.TextField(blank=True, default='')
    yt_trailer_code = models.CharField(max_length=200, blank=True, default='')
    language = models.CharField(max_length=200, blank=True, default='')
    mpa_rating = models.CharField(max_length=200, blank=True, default='')

    background_image = models.CharField(max_length=500, blank=True, default='')
    background_image_original = models.CharField(max_length=500, blank=True, default='')
    small_cover_image = models.CharField(max_length=500, blank=True, default='')
    medium_cover_image = models.CharField(max_length=500, blank=True, default='')
    large_cover_image = models.CharField(max_length=500, blank=True, default='')

    state = models.CharField(max_length=200, blank=True, default='')

    date_uploaded = models.DateTimeField(auto_now=True)
    date_uploaded_unix = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Torrent(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    url = models.CharField(max_length=500, blank=True, default='')
    hash = models.CharField(max_length=500, blank=True, default='')
    quality = models.CharField(max_length=200, blank=True, default='')
    seeds = models.IntegerField(default=0)
    peers = models.IntegerField(default=0)
    size = models.CharField(max_length=200, blank=True, default='')
    size_bytes = models.IntegerField(default=0)
    date_uploaded = models.DateTimeField(auto_now=True)
    date_uploaded_unix = models.IntegerField(default=0)

