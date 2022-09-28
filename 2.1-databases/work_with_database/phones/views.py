from django.shortcuts import render, redirect

from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    if request.GET.get('sort') == 'name':
        phones = Phone.objects.all().order_by('name')
    elif request.GET.get('sort') == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif request.GET.get('sort') == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    phone = Phone.objects.get(slug=slug)
    template = 'product.html'
    context = {'phone': phone}
    return render(request, template, context)
