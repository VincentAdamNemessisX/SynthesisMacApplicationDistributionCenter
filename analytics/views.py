from datetime import datetime, timedelta

from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar

from frontenduser.models import FrontEndUser
from general.common_compute import (get_hot_volume_of_article as g_h_a,
                                    get_hot_volume_of_software as g_h_s)
from general.init_cache import get_all_articles as g_a_as, get_all_software as g_a_s, get_all_user as g_a_u, \
    get_comments


# Create your views here.
def index(request):
    # 获取网站相关指标
    indicators = {}
    recent_appended_user = FrontEndUser.objects.filter(
        django_user__date_joined__gte=datetime.now() - timedelta(days=7)
    )
    indicators['recent_appended_user'] = {'name': '最近新增用户', 'value': len(recent_appended_user)}
    indicators['recent_appended_software'] = {'name': '最近新增软件', 'value': len(g_a_s())}
    indicators['all_user'] = {'name': '总用户数', 'value': len(g_a_u())}
    indicators['all_articles'] = {'name': '总文章数', 'value': len(g_a_as())}
    indicators['all_software'] = {'name': '总软件数', 'value': len(g_a_s())}
    indicators['all_views'] = {'name': '总浏览量',
                               'value': sum([i.view_volume for i in g_a_as()]) + sum([i.view_volume for i in g_a_s()])}
    indicators['all_downloads'] = {'name': '总下载量', 'value': sum([i.download_volume for i in g_a_s()])}
    indicators['all_comments'] = {'name': '总评论数',
                                  'value': len([comment for comment in get_comments()])}
    indicators['all_thumbs'] = {'name': '总点赞数',
                                'value': sum([i.thumbs_volume for i in g_a_as()]) + sum(
                                    [i.thumbs_volume for i in g_a_s()])}
    # 创建一个图表对象
    bar = Bar()
    sorted_software = sorted([s for s in g_a_s()], key=lambda x: g_h_s(x, 1), reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [g_h_s(s, 1) for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("热度", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.download_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.download_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("下载量", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.view_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.view_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("点击量", y_list)
    sorted_software = sorted(sorted_software, key=lambda x: x.thumbs_volume, reverse=True)
    x_list, y_list = [s.name for s in sorted_software][:10], [s.thumbs_volume for s in sorted_software][:10]
    bar.add_xaxis(x_list)
    bar.add_yaxis("点赞", y_list)
    # 设置图表的全局配置项
    bar.set_global_opts(title_opts=opts.TitleOpts(title="软件概览"))
    return render(request, 'index.html',
                  {
                      'chart1': bar.dump_options_with_quotes(),
                      'indicators': indicators
                  })


# @cache_page(60 * 15)
def rank(request):
    all_articles, all_software = g_a_as(), g_a_s()
    today_date = datetime.now().date()
    # compute up and coming star of today
    today_up_and_coming_star_articles, today_up_and_coming_star_software = \
        ([article for article in all_articles if article.updated_time.date() == today_date],
         [software for software in all_software if software.updated_time.date() == today_date])
    today_up_and_coming_star_articles, today_up_and_coming_star_software = \
        (sorted(today_up_and_coming_star_articles, key=lambda x: x.updated_time, reverse=True)[:10],
         sorted(today_up_and_coming_star_software, key=lambda x: x.updated_time, reverse=True)[:10])
    if len(today_up_and_coming_star_software) < 10:
        today_up_and_coming_star_software += [None] * (10 - len(today_up_and_coming_star_software))
    if len(today_up_and_coming_star_articles) < 10:
        today_up_and_coming_star_articles += [None] * (10 - len(today_up_and_coming_star_articles))
    today_popularity_articles, today_popularity_software = (all_articles, all_software)
    for i in today_popularity_articles:
        i.popularity = g_h_a(i, 2)
    for i in today_popularity_software:
        i.popularity = g_h_s(i, 2)

    # compute popularity of today
    today_popularity_articles, today_popularity_software = (
        sorted(today_popularity_articles, key=lambda x: x.popularity, reverse=True)[:10],
        sorted(today_popularity_software, key=lambda x: x.popularity, reverse=True)[:10])
    for i in today_popularity_articles:
        if i.popularity <= 0:
            today_popularity_articles.remove(i)
    for i in today_popularity_software:
        if i.popularity <= 0:
            today_popularity_software.remove(i)
    if len(today_popularity_articles) < 10:
        today_popularity_articles += [None] * (10 - len(today_popularity_articles))
    if len(today_popularity_software) < 10:
        today_popularity_software += [None] * (10 - len(today_popularity_software))

    # compute up and coming star of all time
    all_time_up_and_coming_star_articles, all_time_up_and_coming_star_software = (all_articles, all_software)
    all_time_up_and_coming_star_articles, all_time_up_and_coming_star_software = (
        sorted(all_time_up_and_coming_star_articles, key=lambda x: x.updated_time, reverse=True)[:10],
        sorted(all_time_up_and_coming_star_software, key=lambda x: x.updated_time, reverse=True)[:10])
    if len(all_time_up_and_coming_star_software) < 10:
        all_time_up_and_coming_star_software += [None] * (10 - len(all_time_up_and_coming_star_software))
    if len(all_time_up_and_coming_star_articles) < 10:
        all_time_up_and_coming_star_articles += [None] * (10 - len(all_time_up_and_coming_star_articles))

    # compute popularity of all time
    all_time_popularity_articles, all_time_popularity_software = (all_articles, all_software)
    for i in all_time_popularity_articles:
        i.popularity = g_h_a(i, 1)
    for i in all_time_popularity_software:
        i.popularity = g_h_s(i, 1)
    all_time_popularity_articles, all_time_popularity_software = (
        sorted(all_time_popularity_articles, key=lambda x: x.popularity, reverse=True)[:10],
        sorted(all_time_popularity_software, key=lambda x: x.popularity, reverse=True)[:10])
    for i in all_time_popularity_articles:
        if i.popularity <= 0:
            all_time_popularity_articles.remove(i)
    for i in all_time_popularity_software:
        if i.popularity <= 0:
            all_time_popularity_software.remove(i)
    if len(all_time_popularity_articles) < 10:
        all_time_popularity_articles += [None] * (10 - len(all_time_popularity_articles))
    if len(all_time_popularity_software) < 10:
        all_time_popularity_software += [None] * (10 - len(all_time_popularity_software))
    return render(request, 'rank.html', {
        'today_up_and_coming_star_articles': today_up_and_coming_star_articles,
        'today_up_and_coming_star_software': today_up_and_coming_star_software,
        'today_popularity_articles': today_popularity_articles,
        'today_popularity_software': today_popularity_software,
        'all_time_up_and_coming_star_articles': all_time_up_and_coming_star_articles,
        'all_time_up_and_coming_star_software': all_time_up_and_coming_star_software,
        'all_time_popularity_articles': all_time_popularity_articles,
        'all_time_popularity_software': all_time_popularity_software,
    })
