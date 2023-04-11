from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User - {self.user.username}, Post - {self.post.title}"

