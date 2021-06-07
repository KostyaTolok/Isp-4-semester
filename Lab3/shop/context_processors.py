from products.models import Category


def categories(request):
    cats = Category.objects.all()

    return {'categories': cats}
