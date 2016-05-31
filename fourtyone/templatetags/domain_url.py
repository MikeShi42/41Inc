from django import template
from django.core.urlresolvers import reverse_lazy
from django.contrib.sites.models import Site

from fourtyone.settings import ADMIN_DOMAIN, ADMIN_URLCONF, ROOT_URLCONF

register = template.Library()


@register.simple_tag
def domain_url(route, **kwargs):
    """Helps with switching between main site and client sites.

    Because client sites and the main site use two separate URLconfs, named
    routes in one can't be resolved in the other, so need to load appropriate
    URLconf (either client or admin URLconf) if linking across sites.

    Examples:
        To get the video creation form in the admin panel for a client site:
            <a href="{% domain_url admin_url_for_site=website_id %}></a>
        where website_id = get_current_site(self.request).id

        To link to a client site from a URL in the admin URLconf:
            <a href="{% domain_url client_site=website_id %}></a>
        where website_id is the site ID of some client site.
    """
    if 'admin_url_for_site' not in kwargs and 'client_site' not in kwargs:
        raise ValueError('Pass in either admin_url_for_site or client_site parameter.')

    if 'admin_url_for_site' in kwargs and 'client_site' in kwargs:
        raise ValueError('admin_url_for_site and client_site named parameters are mutually exclusive.')

    if 'client_site' in kwargs:
        # Switches to the client site from the admin site.
        site = Site.objects.get(pk=kwargs['client_site'])
        uri = reverse_lazy(route, urlconf=ROOT_URLCONF)
    else:
        # Switches to the admin site from a client site since the admin site
        # requires website_id in its URL.
        site = Site.objects.get(domain=ADMIN_DOMAIN)
        uri = reverse_lazy(route, urlconf=ADMIN_URLCONF, kwargs={'website_id': kwargs['admin_url_for_site']})

    absolute_url = 'http://%s%s' % (site.domain, uri)

    return absolute_url

