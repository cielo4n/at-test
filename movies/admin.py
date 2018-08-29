from django.contrib import admin
from .models import Genre, Movie, Torrent


class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_uploaded']


class TorrentAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'date_uploaded']

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Torrent, TorrentAdmin)
