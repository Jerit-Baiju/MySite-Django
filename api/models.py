from django.db import models

# Create your models here.

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='image_uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
