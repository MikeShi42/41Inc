# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from websites.forms import WebsiteForm


class WebsiteView(FormView):
    template_name = 'websites/create.html'
    form_class = WebsiteForm
