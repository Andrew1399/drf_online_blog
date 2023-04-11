from django.db import models
from django.contrib.auth.models import User


class Following(models.Model):
    user_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='unique_followers')
        ]
        ordering = ('-created', )

    def count_followers(self):
        return self.following_user_id.count.all()

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"
