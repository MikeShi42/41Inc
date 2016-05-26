from django.http import HttpResponse

from django.views.generic import TemplateView
from django.shortcuts import render


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self):
        user = self.request.user
        context = {}
        context['user'] = user
        context['series'] = user.series.all()
        print context
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)