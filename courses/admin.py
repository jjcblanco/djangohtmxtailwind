from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','access']
    list_filter =['status','display']
    fields = ['title','description','status', 'image','access']

def display_image(self.*args,**kwargs):
    print(obj.image.url)
    url = obj.image.url
    
    return format_html("<img src'{url}' />")

admin.site.register(Course,CourseAdmin) # this will add the Course model to the admin panel
# we can now create, update and delete courses from the admin panel
