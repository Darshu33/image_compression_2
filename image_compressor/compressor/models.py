from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='original/')
    compressed_image = models.ImageField(upload_to='compressed/', blank=True, null=True)

    def __str__(self):
        return self.image.name

