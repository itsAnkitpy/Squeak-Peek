import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_user', blank=True, through=PostLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_repost(self):
        return self.parent != None

    def serialize(self):
        return {
            "id":self.id,
            "content": self.content,
            "likes": random.randint(0,100)
        }
