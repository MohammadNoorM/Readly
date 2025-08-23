from django.shortcuts import redirect
from store.models import Cart, Product, Orders
from .forms import UserInfoForm
from django.core.mail import send_mail
from django.template.loader import render_to_string



def make_order(request):
    if request.method != "POST":
        return redirect("store.checkout")
    
    form = UserInfoForm(request.POST)
    if form.is_valid():
        cart = Cart.objects.filter(session=request.session.session_key).last()
        products = Product.objects.filter(pk__in=cart.items)
        
        total = 0
        for item in products:
            total += item.price

        if total <= 0:
            return redirect("store.cart")
        

        order = Orders.objects.create(customer=form.cleaned_data, total=total)
        for product in products:
            order.orderitem_set.create(product_id=product.id, price=product.price)
        
        send_order_confirmation_email(order, products)
        cart.delete()
        return redirect('store.checkout_complete')
    else:
        return redirect('store.checkout')



def send_order_confirmation_email(order, products):
    subject = f"Order Confirmation - {order.id}"
    message = render_to_string('emails/order.html', {
        'order': order,
        'products': products
    })
    from_email = "no-reply@yourstore.com"
    recipient_list = ['customer@example.com']

    send_mail(subject, html_message=message, message=message, from_email=from_email, recipient_list=recipient_list)