import time
from django.conf import settings
from django.utils.cache import patch_vary_headers

class MultiHostMiddleware:

    def process_request(self, request):
        try:
            request.META["LoadingStart"] = time.time()
            host = request.META["HTTP_HOST"]
            #if host[-3:] == ":80":
            #    host = host[:-3] # ignore default port number, if present

            # best way to do this.
            host_port = host.split(':')
            if len(host_port)==2:
                host = host_port[0]

            if host in settings.HOST_MIDDLEWARE_URLCONF_MAP:
                request.urlconf = settings.HOST_MIDDLEWARE_URLCONF_MAP[host]
                request.META["MultiHost"] = str(request.urlconf)
            else:
                request.META["MultiHost"] = str(settings.ROOT_URLCONF)

        except KeyError:
            pass # use default urlconf (settings.ROOT_URLCONF)

    def process_response(self, request, response):
        if 'MultiHost' in request.META:
            response['MultiHost'] = request.META.get("MultiHost")

        if 'LoadingStart' in request.META:
            _loading_time = time.time() - int(request.META["LoadingStart"])
            response['LoadingTime'] = "%.2fs" % ( _loading_time, )

        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response