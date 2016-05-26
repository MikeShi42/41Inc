from django.http import HttpResponse

from django.views.generic import TemplateView
from django.shortcuts import render
from websites.models import Info


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self):
        user = self.request.user
        context = {
            'user': user,
            'series': user.series.all(),
            'websites': Info.objects.filter(creator_id=user.id)
        }
        print context
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)