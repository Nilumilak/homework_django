from rest_framework import serializers
from django.conf import settings

from students.models import Course, Student, CourseStudents


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'birth_date']


class CourseStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStudents
        fields = ['course', 'student']

    def validate(self, data):
        if data['course'].course_students.count() >= settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Cannot have more than 20 students on course')

        return data


class CourseSerializer(serializers.ModelSerializer):
    course_students = CourseStudentsSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "course_students")
