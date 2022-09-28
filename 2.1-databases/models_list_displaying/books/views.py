from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Book


books = Book.objects.all().order_by('pub_date')


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': books}
    return render(request, template, context)


def books_date(request, pd):
    template = 'books/books_list.html'

    current_book = books.filter(pub_date=pd)

    if list(books).index(current_book[0]) != 0:
        previous_date = Book.objects.get(name=list(books)[list(books).index(current_book[0]) - 1].name).pub_date
    else:
        previous_date = None
    if list(books).index(current_book[0]) < len(books) - 1:
        if len(current_book) > 1:
            next_date = Book.objects.get(name=list(books)[list(books).index(current_book[len(current_book) - 1]) + 1].name).pub_date
        else:
            next_date = Book.objects.get(name=list(books)[list(books).index(current_book[0]) + 1].name).pub_date
    else:
        next_date = None

    context = {'books': current_book, 'previous_date': previous_date, 'next_date': next_date}

    return render(request, template, context)
