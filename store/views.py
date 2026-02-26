from django.shortcuts import render
from .models import Product, Slider, Category, Cart
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.translation import gettext as _

def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return render(request, 'index.html', {'products': products, 'slides': slides})


def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {'product': product})

def category(request, category_id=None):
    cat = None
    query = request.GET.get('q')
    category_id = request.GET.get('category', category_id)
    where = {}

    if query:
        where['name__icontains'] = query
    
    if category_id:
        cat = Category.objects.get(id=category_id)
        where['category_id'] = category_id
    
    products = Product.objects.filter(**where)
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'category.html',
                  {'category': cat, 
                   'page_obj': page_obj})

def cart(request):
    return render(request, 'cart.html')

def cart_update(request, product_id):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[product_id])
    elif product_id not in cart_model.items:
        cart_model.items.append(product_id)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been added to your cart'),
        'items_count': len(cart_model.items)
    })


def cart_remove(request, product_id):
    session_key = request.session.session_key

    if not session_key:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session=session_key).last()
    if not cart_model:
        return JsonResponse({})
    
    elif product_id in cart_model.items:
        cart_model.items.remove(product_id)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been removed from your cart'),
        'items_count': len(cart_model.items)
    })

def checkout(request):
    return render(request, 'checkout.html')

def checkout_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()
    return render(request, 'checkout-complete.html')


def search_api(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    filters = {}

    if query:
        filters['name__icontains'] = query
    if category_id:
        filters['category_id'] = category_id

    products = Product.objects.filter(**filters).select_related('author')[:10]
    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'author': str(p.author) if p.author else '',
            'price': p.price,
            'image': p.image.url if p.image else '',
        })
    return JsonResponse({'results': results})