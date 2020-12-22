from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cache_page_per_user.utils import clear_cache
from cache_page_per_user.utils import get_cache_key


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
    custom_query = get_cache_key('cached_post_with_signal', instance.author_id)
    clear_cache('cached_post_with_signal', custom_query)
