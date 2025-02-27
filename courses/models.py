from django.db import models
import helpers
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

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
    
def get_public_id_prefix(instance,*args, **kwargs):
    print(args)
    print(kwargs)
    title = instance.title
    if title:
        slug= slugify(title)
        return f"courses/{slug}"
    if instance.id:
        return f"courses/{instance.id}"
    return "courses"

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    #image = models.ImageField(upload_to=handle_uploaded_file, null=True, blank=True)
    image = CloudinaryField("image",null=True)
    public_is_prefix = get_public_id_prefix()
    access = models.CharField(max_length=10, choices = AccessRequierements.choices,default=AccessRequierements.ANYONE)
    status = models.CharField(max_length=10, choices = PublishStatus.choices,default=PublishStatus.DRAFT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #slug = models.SlugField(null=True, blank=True)

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


'''lesson model'''
# Lesson.objects.create(title="Lesson 1", description="This is the first lesson", course=course)
# Lesson.ojbects.all()
# Lesson.objects.filter(course=course)
# Lesson.objects.filter(course=course).first()
# Lesson.objects.filter(course=course).last()
# Lesson.objects.filter(course=course).order_by('position')
# Lesson.objects.filter(course=course).order_by('-position')
# Lesson.objects.filter(course=course).order_by('position').first()
# Lesson.objects.filter(course=course).order_by('position').last()
# Lesson.objects.filter(course=course).order_by('position').first().position
# Lesson.objects.filter(course=course).order_by('position').last().position
# Lesson.objects.filter(course=course).order_by('position').first().title

class Lesson(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    can_preview = models.BooleanField(default=False, help_text="This lesson can be previewed by anyone")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices = PublishStatus.choices,default=PublishStatus.DRAFT)
    position = models.IntegerField(default=0)
    #video_url = models.URLField(null=True, blank=True,null=True)  
    video = CloudinaryField("video",null=True,resource_type="video")
    video_duration = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    thumbnail = CloudinaryField("image",null=True)
    free_preview = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order','-updated'] # order by order field

