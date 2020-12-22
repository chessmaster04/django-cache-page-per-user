from django.urls import path

from tests.posts.views import cached_post
from tests.posts.views import cached_post_with_signal
from tests.posts.views import post

urlpatterns = [
    path('post/<int:pk>/', post, name='post_get_or_update'),
    path('cached_post/<int:pk>/', cached_post, name='cached_post_get_or_update'),
    path('cached_post_with_signal/<int:pk>/', cached_post_with_signal, name='cached_post_with_signal_get_or_update'),
]
