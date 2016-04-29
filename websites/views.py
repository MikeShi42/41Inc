# Create your views here.
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.views.generic import CreateView

from websites.forms import WebsiteForm
from websites.models import Website


class WebsiteCreate(SuccessMessageMixin, CreateView):
    template_name = 'websites/create.html'
    form_class = WebsiteForm
    model = Website
    success_message = "%(name)s was created successfully"
    success_url = '/websites/create'
