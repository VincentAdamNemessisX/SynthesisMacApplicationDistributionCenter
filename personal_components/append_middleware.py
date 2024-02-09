from django.utils.deprecation import MiddlewareMixin

from general.init_cache import get_hot_articles_and_software, get_all_category


class AppendMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(AppendMiddleware, self).__init__(*args, **kwargs)
        self.user = None

    def process_request(self, request):
        hot_articles, hot_software = get_hot_articles_and_software()
        if hot_articles is None:
            hot_articles = []
        if hot_software is None:
            hot_software = []
        request.hot_articles, request.hot_software = hot_articles[:3], hot_software[:3]
        request.categories = get_all_category()

    def process_response(self, request, response):
        return response
