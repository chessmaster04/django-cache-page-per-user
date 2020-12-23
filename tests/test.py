import json

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from tests.posts.factories import BaseModelFactory
from tests.posts.models import CachedPost
from tests.posts.models import CachedPostWitHSignal
from tests.posts.models import Post
from tests.posts.serializers import serialize_post


class UserFactory(BaseModelFactory):

    class Meta:
        model = User


class PostFactory(BaseModelFactory):

    class Meta:
        model = Post


class CachedPostFactory(BaseModelFactory):

    class Meta:
        model = CachedPost


class CachedPostWitHSignalFactory(BaseModelFactory):

    class Meta:
        model = CachedPostWitHSignal


class CachePageTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user1 = UserFactory(username='User1')
        cls.user1.set_password('password')
        cls.user1.save()

        cls.user2 = UserFactory(username='User2')
        cls.user2.set_password('password')
        cls.user2.save()

        cls.post = PostFactory(author_id=cls.user1.id, text='old text')
        cls.cached_post = CachedPostFactory(author_id=cls.user1.id, text='old text')
        cls.cached_post_with_signal = CachedPostWitHSignalFactory(author_id=cls.user1.id, text='old text')

        cls.cached_post2 = CachedPostFactory(author_id=cls.user2.id, text='old text')
        cls.cached_post_with_signal2 = CachedPostWitHSignalFactory(author_id=cls.user2.id, text='old text')

        cls.url_post = lambda self, pk: reverse('post_get_or_update', args=(pk,))
        cls.url_cached_post = lambda self, pk: reverse('cached_post_get_or_update', args=(pk,))
        cls.url_cached_post_with_signal = lambda self, pk: reverse('cached_post_with_signal_get_or_update', args=(pk,))

        cls.client = Client()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_not_cached_post(self):
        post = self.post
        url = self.url_post(post.id)

        # auth
        login = self.client.login(username=self.user1.username, password='password')
        self.assertTrue(login)

        # make cache
        response_fetch = self.client.get(url)
        response_fetch_body = response_fetch.json()
        self.assertEqual(response_fetch.status_code, 200)
        self.assertDictEqual(response_fetch_body, serialize_post(post))

        # make update
        new_post_data = {
            'text': 'new text',
        }
        response_update = self.client.put(url, json.dumps(new_post_data))
        response_update_body = response_update.json()
        self.assertDictEqual(response_update_body, {**serialize_post(post), **new_post_data})

        # check cached post
        response_fetch2 = self.client.get(url)
        response_fetch2_body = response_fetch2.json()
        self.assertNotEqual(response_fetch2_body, serialize_post(post))

    def test_cached_post(self):
        post = self.cached_post
        post2 = self.cached_post2
        url = self.url_cached_post(post.id)
        url2 = self.url_cached_post(post2.id)

        # auth 1
        login = self.client.login(username=self.user1.username, password='password')
        self.assertTrue(login)

        # make cache 1
        response_fetch = self.client.get(url)
        response_fetch_body = response_fetch.json()
        self.assertEqual(response_fetch.status_code, 200)
        self.assertDictEqual(response_fetch_body, serialize_post(post))

        # auth 2
        login2 = self.client.login(username=self.user2.username, password='password')
        self.assertTrue(login2)

        # make cache 2
        response_fetch2 = self.client.get(url2)
        response_fetch_body2 = response_fetch2.json()
        self.assertEqual(response_fetch2.status_code, 200)
        self.assertDictEqual(response_fetch_body2, serialize_post(post2))

        # auth 1
        self.client.login(username=self.user1.username, password='password')

        # make update 1
        new_post_data = {
            'text': 'new text',
        }
        response_update = self.client.put(url, json.dumps(new_post_data))
        response_update_body = response_update.json()
        self.assertDictEqual(response_update_body, {**serialize_post(post), **new_post_data})

        # check cached post 1
        response_fetch2 = self.client.get(url)
        response_fetch2_body = response_fetch2.json()
        self.assertEqual(response_fetch2_body, serialize_post(post))

    def test_cached_post_with_signal(self):
        post = self.cached_post_with_signal
        url = self.url_cached_post_with_signal(post.id)
        post2 = self.cached_post_with_signal2
        url2 = self.url_cached_post_with_signal(post2.id)

        # auth 1
        login = self.client.login(username=self.user1.username, password='password')
        self.assertTrue(login)

        # make cache 1
        response_fetch = self.client.get(url)
        response_fetch_body = response_fetch.json()
        self.assertEqual(response_fetch.status_code, 200)
        self.assertDictEqual(response_fetch_body, serialize_post(post))

        # auth 2
        login2 = self.client.login(username=self.user2.username, password='password')
        self.assertTrue(login2)

        # make cache 2
        response_fetch2 = self.client.get(url2)
        response_fetch_body2 = response_fetch2.json()
        self.assertEqual(response_fetch2.status_code, 200)
        self.assertDictEqual(response_fetch_body2, serialize_post(post2))

        # auth 1
        self.client.login(username=self.user1.username, password='password')

        # make update 1
        new_post_data = {
            'text': 'new text',
        }
        response_update = self.client.put(url, json.dumps(new_post_data))
        response_update_body = response_update.json()
        self.assertDictEqual(response_update_body, {**serialize_post(post), **new_post_data})

        # check cached post
        response_fetch2 = self.client.get(url)
        response_fetch2_body = response_fetch2.json()
        self.assertNotEqual(response_fetch2_body, serialize_post(post))
