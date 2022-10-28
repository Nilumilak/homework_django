import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user('admin')


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_students(client, student_factory):
    students = student_factory(_quantity=5)
    url = reverse('students-list')
    response = client.get(url)

    assert response.status_code == 200
    assert all([student.name == response.data[num]['name'] for num, student in enumerate(students)])
    assert len(students) == len(response.data)


@pytest.mark.django_db
def test_get_student(client, student_factory):
    students = student_factory(_quantity=5)
    student = students[3]
    url = reverse('students-detail', args=[student.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert student.name == response.data['name']


@pytest.mark.django_db
def test_create_student(client):
    context = {'name': 'test_student'}
    url = reverse('students-list')
    response_post = client.post(url, context)
    response_get = client.get(url, context)
    assert response_post.status_code == 201
    assert response_get.data[0]['name'] == 'test_student'


@pytest.mark.django_db
def test_update_student(client, student_factory):
    students = student_factory(_quantity=5)
    for num, student in enumerate(students):
        context = {'name': f'test_student{num}'}
        url = reverse('students-detail', args=[student.pk])
        response = client.put(url, context)
        assert response.status_code == 200
        url = reverse('students-detail', args=[student.pk])
        response = client.get(url)
        assert response.data['name'] == context['name']


@pytest.mark.django_db
def test_delete_student(client, student_factory):
    student = student_factory(_quantity=1)
    url = reverse('students-detail', args=[student[0].pk])
    respond = client.delete(url)
    assert respond.status_code == 204
    respond = client.get(url)
    assert respond.status_code == 404
