import os
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from .serializers import PhotoSerializer
from rest_framework.parsers import MultiPartParser
from .models import Photo
from .auth import CustomJwtAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response


class PostPhoto(APIView):

    def post(self, request):
        image = request.data.get("image")
        if image:
            # functionality for posting image goes here
            return Response({"message": "Photo posted", "error":[]})

        try:
            photo = Photo.objects.get(id=request.data["id"])
            return Response({"message": "Photo posted", "error":[]})
        except Photo.DoesNotExist:
            # functionality for posting image goes here
            return Response({"message": "",
                             "error": "Photo Id or uploaded image is required"})


class PhotoViewSet(viewsets.ModelViewSet):

    queryset = Photo.objects.all()

    serializer_class = PhotoSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('published_on', 'user', 'is_draft')

    parser_classes = [MultiPartParser]
    authentication_classes = (CustomJwtAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = PhotoSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            photo = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            photo = self.get_object()
            os.remove(photo.image.path)
            photo.delete()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ordering = request.GET.get("order_by")
        if ordering:
            queryset = queryset.order_by(ordering)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

