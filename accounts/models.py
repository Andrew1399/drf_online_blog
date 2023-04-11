import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Profile(models.Model):
    first_name = models.CharField(max_length=150, db_index=True)
    last_name = models.CharField(max_length=150, db_index=True)
    email = models.EmailField(max_length=150, db_index=True)
    country = models.CharField(max_length=150, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(db_index=True, default='No information...', max_length=550)
    image = models.ImageField(upload_to='images', default='images/avatar.jpg')
    slug = models.SlugField(unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'profile'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    @property
    def filename(self):
        return os.path.basename(self.image.name)