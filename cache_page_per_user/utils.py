from django.core.cache import cache

from cache_page_per_user.constants import DEFAULT_GROUP


def clear_cache(query=None):
    """
    clears cache in redis by query string
    :param query:
    :return:
    """
    def search_key(q):
        def wrapper(key):
            if query in key:
                return 1
            return 0
        return wrapper

    is_low_cache_mem = False
    is_redise = False
    try:
        keys = cache.keys('*')
        is_redise = True
    except AttributeError:
        keys = list(cache._cache.keys())
        is_low_cache_mem = True

    if is_redise:
        cache.delete_many(list(filter(search_key(query), keys)))
    if is_low_cache_mem:
        for key in list(filter(search_key(query), keys)):
            del cache._cache[key]


def get_cache_key(key_prefix, user_id, group=DEFAULT_GROUP, versioned=False, versions_timeout=864000):
    """
    returns
    :param key_prefix:
    :param user_id:
    :param group:
    :param versioned:
    :param versions_timeout:
    :return:
    """
    group_version = cache.get_or_set(group, 1, timeout=versions_timeout) if versioned else 0
    return f'{key_prefix}:{group}:{group_version}:user-{user_id}'
