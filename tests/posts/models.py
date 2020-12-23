from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cache_page_per_user.utils import clear_cache
from cache_page_per_user.utils import get_cache_key
from tests.posts.constants import CachePrefixes


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class CachedPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class CachedPostWitHSignal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


@receiver(pre_save, sender=CachedPostWitHSignal)
def create_slug_wrapper(sender, instance, **kwargs):
    query = get_cache_key(CachePrefixes.CACHED_POST_WITH_SIGNAL, instance.author_id)
    clear_cache(query)
