import json

from django.http import JsonResponse

from cache_page_per_user.cache import cache_page_per_user
from tests.posts.constants import CachePrefixes
from tests.posts.models import CachedPost
from tests.posts.models import CachedPostWitHSignal
from tests.posts.models import Post
from tests.posts.serializers import serialize_post


def _post(request, pk, entity):
    try:
        if request.method == 'GET':
            return JsonResponse(serialize_post(entity.objects.get(pk=pk, author=request.user)))
        elif request.method == 'PUT':
            post_instance = entity.objects.get(pk=pk, author=request.user)
            post_instance.text = json.loads(request.body).get('text')
            post_instance.save()
            return JsonResponse(serialize_post(post_instance))
    except entity.DoesNotExist:
        return JsonResponse({}, status=404)


def post(request, pk):
    return _post(request, pk, Post)


@cache_page_per_user(60, CachePrefixes.CACHED_POST)
def cached_post(request, pk):
    return _post(request, pk, CachedPost)


@cache_page_per_user(60, CachePrefixes.CACHED_POST_WITH_SIGNAL)
def cached_post_with_signal(request, pk):
    return _post(request, pk, CachedPostWitHSignal)
