from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'yts-movie-list-save/', views.yts_movie_list_save),
    url(r'list/', views.movie_list_view),
    url(r'test/', views.test_view),
]
