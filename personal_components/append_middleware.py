from django.utils.deprecation import MiddlewareMixin

from general.init_cache import get_hot_articles_and_software, get_all_category
from general.common_compute import update_user_recent


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
        if request.user.is_authenticated:
            if '/article/details/' in request.path or '/software/details/' in request.path:
                update_user_recent(request.session.get('logon_user'), request.GET.get('article_id'), request.GET.get('software_id'))

    def process_response(self, request, response):
        return response
