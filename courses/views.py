from django.shortcuts import render
from .import services
from .models import Course

def home_view(request):
    
    return render(request, 'home.html')

# Create your views here.
def course_list_view(request):
    queryset = services.get_publish_courses()
    #return JsonResponse({'courses': list(queryset.values())})
    return render(request, 'courses/course_list.html', {'courses': queryset})
    
def course_detail_view(request):
    queryset = services.get_course_detail()
    return render(request, 'courses/course_detail.html')

def lesson_detail_view(request,course_id=None,lesson_id=None,*args,**kwargs):
    print(course_id,lesson_id)
    queryset = services.get_lesson_detail(course_id,lesson_id)
    if queryset is None:
        return render(request, '404.html')
    context = {
        'object': queryset
    }
    return render(request, 'courses/lesson_detail.html', context)
    

