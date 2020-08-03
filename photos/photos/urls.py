from django.contrib import admin
from django.urls import include, path
from .views import JwtToken
from photo.views import PostPhoto


urlpatterns = [
    path('photos/', include('photo.urls')),
    path('post-photo/', PostPhoto.as_view()),
    path('admin/', admin.site.urls),
    path('get-token/', JwtToken.as_view()),
]