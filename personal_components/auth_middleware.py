from django.utils.deprecation import MiddlewareMixin


class AuthFrontEndUser(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(AuthFrontEndUser, self).__init__(*args, **kwargs)
        self.user = None

    def process_request(self, request):
        if request.user.is_authenticated():
            self.user = request.user
        else:
            self.user = None

    def process_response(self, request, response):
        if self.user:
            response.set_cookie('user_id', self.user.id)
        else:
            response.delete_cookie('user_id')
        return response
