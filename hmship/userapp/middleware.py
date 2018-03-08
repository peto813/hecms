# class TunnelingMiddleware(object):
#     def process_request(self, request):
#         if request.META.has_key('HTTP_X_METHODOVERRIDE'):
#             http_method = request.META['HTTP_X_METHODOVERRIDE']
#             if http_method.lower() == 'put':
#                 request.method = 'PUT'
#                 request.META['REQUEST_METHOD'] = 'PUT'
#             if http_method.lower() == 'delete':
#                 request.method = 'DELETE'
#                 request.META['REQUEST_METHOD'] = 'DELETE'
#         return None

class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.META.has_key('HTTP_METHODOVERRIDE'):
            http_method = request.META['HTTP_METHODOVERRIDE']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
        #return None
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
        #return None