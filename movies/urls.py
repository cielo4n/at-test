from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'yts-movie-list-save/', views.yts_movie_list_save)
]
