from django.shortcuts import render
from .import services
from .models import Course
from django.http import Http404, JsonResponse

def home_view(request):
    
    return render(request, 'home.html')


def course_list_view(request):
    queryset = services.get_publish_courses()
    context = {
        "object_list": queryset
    }
    template_name = "courses/list.html"
    if request.htmx:
        template_name = "courses/snippets/list-display.html"
        context['queryset'] = queryset[:3]
    return render(request, template_name, context)

def course_detail_view(request, course_id=None, *args, **kwarg):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset,
    }
    # return JsonResponse({"data": course_obj.id, 'lesson_ids': [x.path for x in lessons_queryset] })
    return render(request, "courses/detail.html", context)


def lesson_detail_view(request,course_id=None,lesson_id=None,*args,**kwargs):
    print(course_id,lesson_id)
    queryset = services.get_lesson_detail(course_id,lesson_id)
    if queryset is None:
        return render(request, '404.html')
    template_name ="courses/lesson-comming-soon.html"
    if not queryset.is_comming_soon:
        template_name = "courses/lesson.html"
    context = {
        'object': queryset
    }
    return render(request, 'courses/lesson.html', context)
    

