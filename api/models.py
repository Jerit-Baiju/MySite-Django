from django.db import models

# Create your models here.

class Image(models.Model):
    user = models.ForeignKey('base.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()
    
    class Meta:
        ordering = ['-created_at']
    

class Unknown(models.Model):
    image = models.ImageField(upload_to='Unknowns')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']