import jwt
from django.http import HttpResponse
from django.views import View
from .settings import SECRET_KEY
from user.models import User


class JwtToken(View):

    def get(self, request):
        username = request.GET.get("username")
        user = User.get_user_by_name(name=username)
        if not user:
            return HttpResponse("User does not exist")

        encoded_token = jwt.encode({'username': username}, SECRET_KEY,
                                   algorithm='HS256')
        return HttpResponse(encoded_token)

