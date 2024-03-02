from datetime import datetime

from django.shortcuts import render

from general.common_compute import (get_hot_volume_of_article as g_h_a,
                                    get_hot_volume_of_software as g_h_s)
from general.init_cache import get_all_articles as g_a_as, get_all_software as g_a_s


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
