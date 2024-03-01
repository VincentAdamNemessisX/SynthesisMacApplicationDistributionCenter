from commentswitharticles.models import Article
from software.models import SoftWare
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_hot_volume_of_article(article_id):
    hot_volume: int = 0
    try:
        article = Article.objects.get(id=article_id, state=2)
        hot_volume += article.updated_time.timestamp() / 1000000 + 10
        hot_volume += article.view_volume * 10 + article.thumbs_volume * 50
        hot_volume += article.comment_set.count() * 200
        hot_volume += article.correlation_software.download_volume * 30
    except ValueError:
        pass
    except TypeError:
        pass
    except AttributeError:
        pass
    return int(hot_volume)


def get_hot_volume_of_software(software_id):
    hot_volume: int = 0
    try:
        software = SoftWare.objects.get(id=software_id, state=2)
        hot_volume += software.updated_time.timestamp() / 1000000 + 10
        hot_volume += software.view_volume * 10 + software.thumbs_volume * 50
        hot_volume += software.download_volume * 200
        hot_volume += software.comment_set.count() * 100
        hot_volume += software.article_set.count() * 20
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
