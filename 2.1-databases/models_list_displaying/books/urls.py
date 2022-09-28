from django.urls import path

from . import views, converters
from django.urls import register_converter


register_converter(converters.PubDateConverter, 'pub_date')

urlpatterns = [
    path('', views.books_view),
    path('books/', views.books_view),
    path('books/<pub_date:pd>/', views.books_date, name='book_filter'),
]
