# django-cache-page-per-user
Extending the Django's [`cache_page`](https://docs.djangoproject.com/en/dev/topics/cache/#the-per-view-cache) decorator.
Supports caching per user and per language.
Support custom settings and clearing cache.

Support of caches
- django_redis.cache.RedisCache
- django.core.cache.backends.locmem.LocMemCache

## Installation
Run `pip install django-cache-page-per-user`

## Usage
Use prefixes to group views by the common models they depend on.

```python
# constants.py
class CachePrefixes:
    AUTHOR = 'AUTHOR'
    ARTICLE = 'ARTICLE'
    COMMENT = 'COMMENT'
```
Use @cache_page_per_user like @cache_page, this decorator will cache responses with only safe methods and with status 200
```python
# view.py
from cache_page_per_user.cache import cache_page_per_user
from django.utils.decorators import method_decorator
from constants import CachePrefixes

@cache_page_per_user(60*60, CachePrefixes.ARTICLE)
def article_view(request, pk):
    ...

@cache_page_per_user(60*60, CachePrefixes.ARTICLE)
def article_some_info_view(request, pk):
    ...

@cache_page_per_user(60*60, CachePrefixes.AUTHOR)
def author_view(request, pk):
    ...

# for ViewSet
class CommentViewSet(ViewSet):
    ...
    @method_decorator(cache_page_per_user(60*60, CachePrefixes.COMMENT))
    def retrieve(self, request, pk=None):
        ...

```
Create signals on the model, when changed, the cache will be reset
```python
# signals.py
...
from cache_page_per_user.utils import clear_cache
from cache_page_per_user.utils import get_cache_key
from constants import CachePrefixes
from models.py import Article

...

@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def create_slug_wrapper(sender, instance, **kwargs):
    query = get_cache_key(CachePrefixes.ARTICLE, instance.author_id)
    clear_cache(query)
```
