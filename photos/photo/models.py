from django.db import models
from user.models import User
from django.utils import timezone


class Photo(models.Model):

    caption = models.CharField(max_length=100, null=True)
    published_on = models.DateTimeField(default=timezone.now)
    is_draft = models.BooleanField(default=False)
    image = models.ImageField(upload_to="static/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


