# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.views.generic import FormView

from websites.forms import WebsiteForm
from websites.models import Info


class WebsiteCreate(SuccessMessageMixin, FormView):
    template_name = 'websites/create.html'
    form_class = WebsiteForm
    success_message = "%(name)s was created successfully"
    success_url = '/websites/create'

    def form_valid(self, form):
        self.create_site(form)
        self.create_info(form)
        return super(WebsiteCreate, self).form_valid(form)

    def create_site(self, form):
        site = Site(name=form.cleaned_data["name"], domain=form.cleaned_data["domain"])
        site.save()
        return site

    def create_info(self, form):
        info = Info(description=form.cleaned_data["description"])
        info.save()
        return info
