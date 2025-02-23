from django.db import models
import helpers
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()

# Create your models here.

class AccessRequierements(models.TextChoices): 
    ANYONE = 'any', 'Anyone'
    EMAILREQUIRED = 'email', 'Email Required'
  
class PublishStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PUBLISHED = 'PUBLISHED', 'Published'
    COMMING_SOON = 'soon', 'Comming Soon'
    DRAFT = 'DRAFT', 'Draft'

def handle_uploaded_file(f,file_name):
    
    return f"uploads/{file_name}"
    

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    #image = models.ImageField(upload_to=handle_uploaded_file, null=True, blank=True)
    image = CloudinaryField("image",null=True)
    access = models.CharField(max_length=10, choices = AccessRequierements.choices,default=AccessRequierements.ANYONE)
    status = models.CharField(max_length=10, choices = PublishStatus.choices,default=PublishStatus.DRAFT)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property 
    def image_admin(self):
        if not self.image:
            return ""
        image_options = {	
            "width": 400,
            "height": 400,
            "crop": "fill"
        }
               
        url = self.image.build_url(image_options)
        return url
    
    def image_thumbnail(self,as_html=False,width=400,height=400):
        if not self.image:
            return ""
        image_options = {	
            "width": 400,
            "height": 400,
            "crop": "fill"
        }
        if as_html:
            return self.image.image(**image_options)
            
        url = self.image.build_url(**image_options)
        return url
