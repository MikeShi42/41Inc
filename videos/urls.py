from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='video-index'),
    url(r'^create$', views.VideoCreate.as_view(), name='video-create')
]