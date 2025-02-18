from django.contrib import admin

# Register your models here.
from .models import Course


admin.site.register(Course) # this will add the Course model to the admin panel
# we can now create, update and delete courses from the admin panel
