from django.db import models


class Post(models.Model):
    user = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    text = models.TextField()
    number_of_likes = models.IntegerField(default=0, blank=True)
    created = models.DateTimeField(auto_now_add=True)
