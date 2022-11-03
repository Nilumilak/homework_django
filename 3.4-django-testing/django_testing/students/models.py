from django.db import models


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(Student, blank=True, through='CourseStudents')


class CourseStudents(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_students')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_students')
