from django.apps import apps
from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, PublishStatus




from .models import Course, PublishStatus


def get_publish_courses():
    Course = apps.get_model('courses', 'Course')
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishStatus.PUBLISHED,
            public_id=course_id
        )
    except:
        pass
    return obj

def get_course_lessons(course_obj=None):
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMMING_SOON]
    )
    return lessons

def get_lesson_detail(course_id,lesson_id):
    Lesson = apps.get_model('courses', 'Lesson')
    return Lesson.objects.get_object_or_404(course_id=course_id,id=lesson_id,PublishStatus=PublishStatus.PUBLISHED)

    

