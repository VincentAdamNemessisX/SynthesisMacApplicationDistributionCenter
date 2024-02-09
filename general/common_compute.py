from commentswitharticles.models import Article
from software.models import SoftWare
import datetime


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
