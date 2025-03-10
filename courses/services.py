from django.apps import apps
from django.shortcuts import render, get_object_or_404




from .models import Course, PublishStatus


def get_publish_courses():
    Course = apps.get_model('courses', 'Course')
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_detail(course_id):
    Course = apps.get_model('courses', 'Course')
    return Course.objects.get_object_or_404(id=course_id)

def get_lesson_detail(course_id,lesson_id):
    Lesson = apps.get_model('courses', 'Lesson')
    return Lesson.objects.get_object_or_404(course_id=course_id,id=lesson_id,PublishStatus=PublishStatus.PUBLISHED)

    

