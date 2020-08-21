from .views import post_list
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import Articolo, ThreadTask
from django.utils import timezone
from asgiref.sync import sync_to_async
from django_redis import get_redis_connection
from .thread import *

startThreadTask();

#per eseguire operazioni sulle liste occorre connettersi manualmente a Redis
conn = get_redis_connection("default")

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#la lista dei post viene caricata dalla cache se presente
#viene utilizzata la connessione definita in settings.py
def post_list_cache(request):

    if 'articoli' in cache:
        print('ok')
        posts = cache.get('articoli')
        return render(request, 'blog/post_list.html', {'posts': posts})

    else:
        posts = Articolo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        cache.set('articoli', posts, timeout=CACHE_TTL)
        print('no ok')
        return render(request, 'blog/post_list.html', {'posts': posts})

#in questa pagina vengono visualizzate le ultime azioni eseguite dagli utenti
#sul sito. Le azioni vengono aggiunte su views.py
def news(request):
    if 'news' in conn:
        news = conn.lrange('news', 0, -1)
        for indx, new in enumerate(news):
            news[indx] = new.decode('utf-8')
        return render(request, 'blog/news.html', {'news': news})
    else:
        return render(request, 'blog/news.html', {'news': ["Nothing new"]})
