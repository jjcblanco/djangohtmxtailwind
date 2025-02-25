from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson


# Register your models here.
from .models import Course


class LessonInline(admin.TabularInline): # this will add the Lesson model to the Course admin panel
    model = Lesson  # this will add the Lesson model to the Course admin panel
    extra = 0 # this will add the Lesson model to the Course admin panel
    readonly_fields = ['display_image'] # this will add the Lesson model to the Course admin panel
    def display_image(self, obj):
        # your code here to display the image
        # for example:
        return format_html('<img src="{}" />'.format(obj.thumbnail.url))
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline] # this will add the Lesson model to the Course admin panel
    list_display = ['title', 'status','access']
    list_filter =['status','access']
    fields = ['title','description','status', 'image','access','display_image']
    readonly_fields = ['display_image']

    def display_image(self,obj,*args,**kwargs):
        print(obj.image.url)
        #url = obj.image.url
        cloudinary_id = str(obj.image)
        #otrafroma de hacerlo
        cloudinary_html2 = obj.image.image(width=400, height=400)
        clodinary_html = CloudinaryImage(cloudinary_id).image(width=400, height=400)
        return format_html(cloudinary_html2)
        
        
        
        #return format_html(f"<img src='{url}' />")

    display_image.short_description = 'Image'

#admin.site.register(Course,CourseAdmin) # this will add the Course model to the admin panel
# we can now create, update and delete courses from the admin panel
