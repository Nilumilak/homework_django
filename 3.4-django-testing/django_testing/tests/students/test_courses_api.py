import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture(scope='session')
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def test_with_specific_settings(settings):
    settings.MAX_STUDENTS_PER_COURSE = 1
    assert settings.MAX_STUDENTS_PER_COURSE


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url)

    assert response.status_code == 200
    assert all([course.name == response.data[num]['name'] for num, course in enumerate(courses)])
    assert len(courses) == len(response.data)


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    course = courses[3]
    response1 = client.get(url, {'id': course.id})
    response2 = client.get(url, {'name': course.name})
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert course.name == response1.data[0]['name']
    assert course.name == response2.data[0]['name']


@pytest.mark.django_db
def test_create_course(client):
    context = {'name': 'test_course'}
    url = reverse('courses-list')
    response_post = client.post(url, context)
    response_get = client.get(url, context)
    assert response_post.status_code == 201
    assert response_get.data[0]['name'] == 'test_course'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=5)
    for num, course in enumerate(courses):
        context = {'name': f'test_course{num}'}
        url = reverse('courses-detail', args=[course.pk])
        response = client.put(url, context)
        assert response.status_code == 200
        url = reverse('courses-detail', args=[course.pk])
        response = client.get(url)
        assert response.data['name'] == context['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[course[0].pk])
    respond = client.delete(url)
    assert respond.status_code == 204
    respond = client.get(url)
    assert respond.status_code == 404


@pytest.mark.django_db
def test_check_students_quantity(client, course_factory, student_factory, test_with_specific_settings):
    course = course_factory()
    students = student_factory(_quantity=2)
    url = reverse('course_students-list')
    for num, student in enumerate(students, start=1):
        response = client.post(url, data={'course': course.pk, 'student': student.pk})
        if len(students) > num:
            assert response.status_code == 201
        else:
            assert response.status_code == 400
            assert response.json() == {"non_field_errors": ["Cannot have more than 20 students on course"]}