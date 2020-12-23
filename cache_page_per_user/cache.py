from functools import wraps

from django.core.cache import cache
from django.utils.cache import patch_response_headers

from cache_page_per_user.constants import DEFAULT_GROUP
from cache_page_per_user.constants import SAFE_METHODS


def custom_cache_page(
        ttl,
        key_func,
        key_prefix=None,
        group_func=None,
        versioned=False,
        versions_timeout=864000,
):
    def _cache(view_func):
        @wraps(view_func)
        def __cache(request, *args, **kwargs):
            if getattr(request, 'do_not_cache', False) or request.method not in SAFE_METHODS:
                return view_func(request, *args, **kwargs)
            group = group_func(request) if group_func else None
            group_version = cache.get_or_set(group, 1, timeout=versions_timeout) if versioned else 0
            cache_key = f'{key_prefix}:{group}:{group_version}:{key_func(request)}'
            try:
                response = cache.get(cache_key)
            except KeyError:
                response = None
            process_caching = not response or getattr(request, '_bust_cache', False)
            if process_caching:
                response = view_func(request, *args, **kwargs)
                if response.status_code == 200:
                    patch_response_headers(response, ttl)
                    if hasattr(response, 'render') and callable(response.render):
                        def set_cache(val) -> None:
                            cache.set(cache_key, val, ttl)
                        response.add_post_render_callback(set_cache)
                    else:
                        cache.set(cache_key, response, ttl)
            setattr(request, '_cache_update_cache', False)
            return response
        return __cache
    return _cache


def cache_page_per_user(ttl, key_prefix):
    def key_func(request):
        lang = f'language-{request.LANGUAGE_CODE or ""}'
        user = f'anonymous' if request.user.is_anonymous else f'user-{str(request.user.id)}'
        return f'{user}:{lang}:{request.path}'

    return custom_cache_page(
        ttl=ttl,
        key_func=key_func,
        group_func=lambda r: DEFAULT_GROUP,
        key_prefix=key_prefix,
    )
