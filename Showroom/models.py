from django.db import models

# Create your models here.
from django.utils.timezone import now
# Create your models here.

class Showroom(models.Model):  
    name = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=15, unique=True) 
    registered_at = models.DateTimeField(default=now)  
    approval_status = models.BooleanField(default=False)  
    password = models.CharField(max_length=128)  
    id_proof_number = models.CharField(max_length=50, unique=True)  
    profile_image_showroom = models.ImageField(upload_to='profile_images_showroom/', null=True, blank=True)  
    address = models.TextField() 