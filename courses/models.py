from django.db import models
import uuid
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
    
def generate_public_id(instance,*args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-","")
    if not title:
        return unique_id
    slug= slugify(title)
    unique_id_short = unique_id[:6]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance,*args, **kwargs):
    if hasattr(instance,'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return "Courses"
    return f"courses/{public_id}"

def get_display_name(instance,is_thumbnail = False,*args, **kwargs):
    if hasattr(instance,'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance,'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__

    return f"{model:name} Upload"
get_thumbnail_display_name = lambda instance:get_display_name(instance,is_thumbnail = True)

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    #image = models.ImageField(upload_to=handle_uploaded_file, null=True, blank=True)
    image = CloudinaryField(
        "image",null=True,
        public_id_prefix = get_public_id_prefix,
        display_name = get_display_name,
        tags=["course","thumbnail"]
        )

    access = models.CharField(max_length=10, choices = AccessRequierements.choices,default=AccessRequierements.ANYONE)
    status = models.CharField(max_length=10, choices = PublishStatus.choices,default=PublishStatus.DRAFT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #slug = models.SlugField(null=True, blank=True)
    def save(self, *args, **kwargs):
        #before saving the model
        if self.public_id == "" or self.public_id is None:
            
            self.public_id = generate_public_id(self)
        return super().save()

    def get_absolute_url(self):
        return self.path
    @property
    def path(self):
        return f"courses/{self.public_id}"
    def get_display_name(self):
        return f"{self.title} - Course " 

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
    video = CloudinaryField("video",
                            public_id_prefix = get_public_id_prefix,
                            display_name = get_display_name,
                            tags=["video","lesson"],
                            null=True,resource_type="video")
    video_duration = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True)
    thumbnail = CloudinaryField("image",
                                public_id_prefix = get_public_id_prefix,
                                display_name = get_display_name,
                                tags=["lesson","thumbnail"],
                                null=True)
    free_preview = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order','-updated'] # order by order field

    def save(self, *args, **kwargs):
            #before saving the model
            if self.public_id == "" or self.public_id is None:
                
                self.public_id = generate_public_id(self)
            return super().save()
    @property
    def path(self):
        course_path = self.course.path
        if course_path.startswith("/"):
            course_path = course_path[1:]

        return f"{self.course.path}/lessons/{self.public_id}"
    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}" 