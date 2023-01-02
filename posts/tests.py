from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Post
# Create your tests here.
User = get_user_model()

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword2')
        Post.objects.create(content="my first post", 
            user=self.user)
        Post.objects.create(content="my first post", 
            user=self.user)
        Post.objects.create(content="my first post", 
            user=self.userb)
        self.currentCount = Post.objects.all().count()

    def test_post_created(self):
        post_obj = Post.objects.create(content="my second post", 
            user=self.user)
        self.assertEqual(post_obj.id, 4)
        self.assertEqual(post_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
    
    def test_post_list(self):
        client = self.get_client()
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_post_list(self):
        client = self.get_client()
        response = client.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", 
            {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", 
            {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/posts/action/", 
            {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_repost(self):
        client = self.get_client()
        response = client.post("/api/posts/action/", 
            {"id": 2, "action": "repost"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_post_id = data.get("id")
        self.assertNotEqual(2, new_post_id)
        self.assertEqual(self.currentCount + 1, new_post_id)

    def test_post_create_api_view(self):
        request_data = {"content": "This is my test post"}
        client = self.get_client()
        response = client.post("/api/posts/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_post_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_post_id)
    
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/posts/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/posts/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/posts/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)

