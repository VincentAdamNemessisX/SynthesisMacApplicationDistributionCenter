from django.urls import path

from SynthesisMacApplicationDistributionCenter.urls import urlpatterns

# 定义一个装饰器，接受一个 url 作为参数
def register_url(url):
    # 定义一个内部函数，接受一个 view 函数作为参数
    def decorator(view_func):
        # 将 url 和 view 函数添加到 urlpatterns 列表中
        urlpatterns.append(path(url, view_func))
        # 返回 view 函数
        return view_func

    # 返回内部函数
    return decorator
