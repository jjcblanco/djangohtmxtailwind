import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson


# Register your models here.
from .models import Course


class LessonInline(admin.StackedInline): # this will add the Lesson model to the Course admin panel
    model = Lesson  # this will add the Lesson model to the Course admin panel
    extra = 0 # this will add the Lesson model to the Course admin panel
    readonly_fields = ['public_id','updated','display_image','display_video'] # this will add the Lesson model to the Course admin panel

    
    def display_image(self, obj, *args, **kwargs):
        # your code here to display the image
        # for example:
        url = helpers.get_cloudinary_image_object(obj, field_name="thumnail", as_html=False, width=200, height=200)
        return format_html(f"<img src={url} />")
    
    display_image.short_description = 'Thumbnail'
    
    def display_video(self, obj, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj, 
            field_name='video',
            as_html=True,
            width=550
        )
        return format_html(f"{url}")
    
    display_video.short_description = 'Video'
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline] # this will add the Lesson model to the Course admin panel
    list_display = ['title', 'status','access']
    list_filter =['status','access']
    fields = ['public_id','title','description','status', 'image','access','display_image','updated']
    readonly_fields = ['public_id','display_image','updated']

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj, 
            field_name='image',
            width=200
        )
        return format_html(f"<img src={url} />")

    display_image.short_description = "Current Image"

#admin.site.register(Course,CourseAdmin) # this will add the Course model to the admin panel
# we can now create, update and delete courses from the admin panel
