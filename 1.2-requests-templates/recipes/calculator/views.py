from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def recipe(request, dish):
    dishes = DATA.get(dish)
    servings = request.GET.get('servings')
    if dishes and servings and servings.isdigit():
        dishes = {item: quantity * int(servings) for item, quantity in dishes.items()}
    context = {
        'recipe': dishes
    }
    return render(request, 'calculator/index.html', context)


