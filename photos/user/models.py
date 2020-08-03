from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)

    @classmethod
    def get_user_by_name(cls, name):
        try:
            return User.objects.get(name=name)
        except User.DoesNotExist:
            return None

