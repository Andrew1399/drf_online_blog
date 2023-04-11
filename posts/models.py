from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True,)
    read_time = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(User, related_name='likes', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', '-updated']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def count_likes(self):
        return self.liked.count()

