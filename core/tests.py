# python manage.py test --keepdb --verbosity=3 core

import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient


# Create your tests here.
from core.models import Blog


class GlobalSetup(APITestCase):
    """
    Ensure we can run server
    """

    def setUp(self):
        self.client = APIClient()
        user = authenticate(username='admin', password='admin')
        print(user)
        self.user = User.objects.get(id=user.id)
        token, create = Token.objects.get_or_create(user=self.user)
        self.token = token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token.key)
        self.header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token.key)}
        print(self.header)
        self.search = {'search': '', 'page': 1, 'size': 5}


class BlogTestCases(GlobalSetup):

    def test_create_update(self):
        # Data
        data = {
                "title" : "Django Tutorial",
                "content" : "It contains about the overview of django framework",
            }

        # create blog
        url = reverse('blog_create')
        self.post = self.client.post(url, data, format='json', **self.header)
        self.assertEqual(self.post.status_code, status.HTTP_201_CREATED)
        print(self.post.data)

        comment_data = {
            "blog_id": self.post.data['id'],
            "comment": "Excellent tutorial"
        }

        # create comment
        url = reverse('comments_create')
        self.comment_post = self.client.post(url, comment_data, format='json', **self.header)
        self.assertEqual(self.comment_post.status_code, status.HTTP_201_CREATED)
        print(self.comment_post.data)

        # retrieve blog
        url = reverse('blog_retrieve', args=[self.post.data['id']])
        self.get = self.client.get(url, format='json', **self.header)
        self.assertEqual(self.get.status_code, status.HTTP_200_OK)

        # update blog
        url = reverse('blog_update_delete', args=[self.post.data['id']])
        data['title'] = "Django Tutorial Part 1"
        data['author_id'] = self.post.data['author_id']
        self.put = self.client.put(url, data, format='json', **self.header)
        print(self.put.data)
        self.assertEqual(self.put.status_code, status.HTTP_200_OK)

        # delete blog
        url = reverse('blog_update_delete', args=[self.post.data['id']])
        self.delete = self.client.delete(url, format='json', **self.header)
        print(self.delete.data)
        self.assertEqual(self.delete.status_code, status.HTTP_200_OK)

    def blog_list(self):
        # list
        url = reverse('blog_list')
        self.get = self.client.get(url, self.search, format='json', **self.header)
        data = json.loads(json.dumps(self.get.data))
        orm_list_count = len(Blog.objects.all()[:5])
        print(orm_list_count)
        self.assertEqual(self.get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), orm_list_count)

