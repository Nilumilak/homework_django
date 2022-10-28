from rest_framework import serializers

from students.models import Course, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'birth_date']


class CourseSerializer(serializers.ModelSerializer):
    students = StudentSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "students")
