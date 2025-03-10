from django.shortcuts import render
from .import services
from .models import Course

# Create your views here.
def course_list_view(request):
    queryset = services.get_publish_courses()
    return render(request, 'courses/course_list.html')
def course_detail_view(request):
    return render(request, 'courses/course_detail.html')

def lesson_detail_view(request):
    return render(request, 'courses/lesson_detail.html')

