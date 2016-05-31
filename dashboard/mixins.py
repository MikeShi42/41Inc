class SiteIdMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SiteIdMixin, self).get_context_data(**kwargs)
        context['site_id'] = self.kwargs['pk']
        return context