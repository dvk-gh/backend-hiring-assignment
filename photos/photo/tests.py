import io
import os
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from photo.models import Photo


class PhotoApiTest(APITestCase):

    def setUp(self):    
        self.user = User.objects.create(name="abc", email="def", password="def123")
        self.client.force_authenticate(user=self.user)

        for data in [{'image': self.get_image(100, 100), "is_draft": True,
                      'caption': "test_caption", "user": self.user.id},
                {'image': self.get_image(100, 100), "is_draft": False,
                 'caption': "test_caption", "user": self.user.id}]:
            self.client.post("/photos/", data, format='multipart')

        photos = Photo.objects.all()
        self.photo_created_first = photos[0]
        self.photo_created_second = photos[1]


    def tearDown(self):
        for img_name in os.listdir("static"):
            os.remove("static/"+img_name)

    def get_image(self, width, height):
        img_file = io.BytesIO()
        image = Image.new(mode='RGB', size=(width, height))
        image.save(img_file, 'png')
        img_file.name = 'image_test.png'
        img_file.seek(0)
        return img_file

    def test_create_photo(self):
        data = {'image': self.get_image(200, 200),
                'caption': "test_caption", "user": self.user.id}

        response = self.client.post("/photos/", data, format='multipart')
        self.assertEqual(response.data["caption"], data["caption"])
        self.assertEqual(response.data["user"], data["user"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_photo_invalid_image(self):
        data = {'image': self.get_image(20000, 20000),
                'caption': "test_caption", "user": self.user.id}

        response = self.client.post("/photos/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_photo_valid(self):
        url = "/photos/{}/".format(self.photo_created_first.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_photo_invalid_id(self):
        url = "/photos/1234/"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_photo(self):
        url = "/photos/{}/".format(self.photo_created_first.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_photo_invalid(self):
        url = "/photos/199999/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_photos(self):
        response = self.client.get("/photos/")
        self.assertEqual(response.data[0]["id"], self.photo_created_first.id)
        self.assertEqual(response.data[1]["id"], self.photo_created_second.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/photos/?is_draft=true")
        self.assertEqual(response.data[0]["id"], self.photo_created_first.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/photos/?order_by=-published_on")
        self.assertEqual(response.data[0]["id"], self.photo_created_second.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)