from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_num = request.GET.get('page', 1)
    with open('data-398-2018-08-30.csv', 'r', encoding='UTF-8') as f:
        reader = list(csv.DictReader(f))

    paginator = Paginator(reader, 10)

    context = {
        'bus_stations': paginator.get_page(page_num),
        'page': paginator.get_page(page_num),
    }
    return render(request, 'stations/index.html', context)
