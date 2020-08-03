from rest_framework import authentication
from rest_framework import exceptions
import jwt
from user.models import User
from photos.settings import SECRET_KEY


class CustomJwtAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        username = request.META.get("HTTP_USERNAME")
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed('token verification failed')

        if decoded.get("username") != username:
            raise exceptions.AuthenticationFailed('unauthorized user')
        else:
            return User.get_user_by_name(username), None
