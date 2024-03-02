from datetime import datetime, time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_hot_volume_of_article(article, get_type=1):
    hot_volume: int = 0
    try:
        if get_type == 1:
            hot_volume += article.updated_time.timestamp() / 1000000 + 10
            hot_volume += article.view_volume * 10 + article.thumbs_volume * 50
            hot_volume += article.comment_set.count() * 200
            hot_volume += article.correlation_software.download_volume * 30
        if get_type == 2:
            today = datetime.now().date()
            start_time = time(0, 0, 0)  # 设置开始时间为 00:00:00
            end_time = time(23, 59, 59)  # 设置结束时间为 23:59:59
            start_datetime = datetime.combine(today, start_time)  # 组合日期和时间，得到开始日期时间
            end_datetime = datetime.combine(today, end_time)  # 组合日期和时间，得到结束日期时间
            hot_volume += (article.updated_time.timestamp() / 1000000 + 10) \
                if article.updated_time.date() == datetime.now().date() else 0
            hot_volume += article.comment_set.all().filter(
                created_time__range=(start_datetime, end_datetime)).count() * 200
    except ValueError:
        pass
    except TypeError:
        pass
    except AttributeError:
        pass
    except IndexError:
        pass
    return int(hot_volume)


def get_hot_volume_of_software(software, get_type=1):
    hot_volume: int = 0
    try:
        if get_type == 1:
            hot_volume += software.updated_time.timestamp() / 1000000 + 10
            hot_volume += software.view_volume * 10 + software.thumbs_volume * 50
            hot_volume += software.download_volume * 200
            hot_volume += software.comment_set.count() * 100
            hot_volume += software.article_set.count() * 20
        if get_type == 2:
            today = datetime.now().date()
            start_time = time(0, 0, 0)
            end_time = time(23, 59, 59)
            start_datetime = datetime.combine(today, start_time)
            end_datetime = datetime.combine(today, end_time)
            hot_volume += (software.updated_time.timestamp() / 1000000 + 10) \
                if software.updated_time.date() == datetime.now().date() else 0
            hot_volume += software.comment_set.all().filter(
                created_time__range=(start_datetime, end_datetime)).count() * 100
    except ValueError:
        pass
    except TypeError:
        pass
    except AttributeError:
        pass
    return int(hot_volume)


def get_context_articles(articles, article_id):
    context_articles = {'previous': None, 'next': None}
    index = 0
    for i in range(len(articles)):
        if articles[i].id == article_id:
            index = i
            break
    if index > 0:
        context_articles['previous'] = articles[index - 1]
    if index < len(articles) - 1:
        context_articles['next'] = articles[index + 1]
    # print(context_articles)
    return context_articles


def compute_similarity(str1, str2):
    vectorizer = TfidfVectorizer()
    corpus = [str1, str2]
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors[0], vectors[1])
    return similarity[0][0]
