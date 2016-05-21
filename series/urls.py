from django.shortcuts import render
from django.conf.urls import include, url
import series.views 

urlpatterns = [
    url(r"^series/create/$", series.views.create, name="create_series"),  
]
urlpatterns += account.urls.urlpatterns
