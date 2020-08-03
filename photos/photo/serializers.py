import sys
from .models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    # Max size in bytes
    max_size = 20000

    # max height in pixels
    max_width = 1000
    max_height = 1000

    class Meta:
        model = Photo
        fields = "__all__"

    def validate(self, attrs):
        img = attrs.get('image', None)
        if img is not None:
            file_size = sys.getsizeof(img.file)
            if file_size > self.max_size:
                raise serializers.ValidationError("File size exceeds {}".format(self.max_size))
            width, height = img.image.size
            if width > self.max_width:
                raise serializers.ValidationError("File width exceeds {}".format(self.max_width))

            if height > self.max_height:
                raise serializers.ValidationError("File height exceeds {}".format(self.max_height))

        return attrs

