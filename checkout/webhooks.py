from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import stripe
import django_store.settings as settings
from django.http import HttpResponse
from checkout import models
from store.models import Order, Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received





@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    
    if 'HTTP_STRIPE_SIGNATURE' not in request.META:
        print("No Stripe signature header found")
        return HttpResponse(status=400)
    
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        print("Invalid payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        return HttpResponse(status=400)
    
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print("PaymentIntent was successful!")
        
        if 'transaction' in payment_intent.metadata:
            transaction_id = payment_intent.metadata['transaction']
            try:
                make_order(transaction_id)
                print(f"Order created successfully for transaction {transaction_id}")
            except Exception as e:
                print(f"Error creating order for transaction {transaction_id}: {str(e)}")
        else:
            print("No transaction metadata found in payment intent")
    else:
        print(f"Unhandled event type: {event.type}")

    return HttpResponse(status=200)



@csrf_exempt
def paypal_webhook(sender, **kwargs):
    if sender.payment_status == ST_PP_COMPLETED:
        if sender.receiver_email != settings.PAYPAL_EMAIL:
            return
        print('Payment intent was successful')
        make_order(sender.invoice)

valid_ipn_received.connect(paypal_webhook)


def make_order(transaction_id):
    transaction = models.Transaction.objects.get(pk=transaction_id)

    # Guard against duplicate webhook calls
    if Order.objects.filter(transaction=transaction).exists():
        print(f"Order already exists for transaction {transaction_id}, skipping")
        return

    transaction.status = models.TransactionStatus.Completed
    transaction.save()
    print(f"Transaction {transaction_id} marked as completed")
    
    try:
        order = Order.objects.create(transaction=transaction)
    except IntegrityError:
        print(f"Order already exists for transaction {transaction_id} (race condition), skipping")
        return

    products = Product.objects.filter(pk__in=transaction.items)
    for product in products:
        order.orderitem_set.create(product=product, price=product.price)
    
    print(f"Order created with {products.count()} products")

    # Send email separately so a mail error doesn't break the webhook
    try:
        msg_html = render_to_string('emails/order.html', {
            'order': order,
            'products': products
        })

        # Plain text fallback for email clients that don't support HTML
        product_lines = "\n".join(
            f"  - {p.name}: {p.price} $\n    Download: {p.pdf_file_url}" for p in products
        )
        msg_plain = (
            f"Order Confirmation #{order.id}\n"
            f"{'=' * 30}\n\n"
            f"Hi {order.transaction.customer_name},\n\n"
            f"Thank you for your order! Your payment has been confirmed.\n\n"
            f"Your Books:\n{product_lines}\n\n"
            f"Total: {order.transaction.amount} $\n\n"
            f"If you have any questions, simply reply to this email."
        )

        print(f"Sending email to: {order.transaction.customer_email}")
        send_mail(
            subject=f"Readly - Order #{order.id} Confirmed",
            html_message=msg_html,
            message=msg_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.transaction.customer_email],
            fail_silently=False,
        )
        print("Email sent successfully")
    except Exception as e:
        print(f"Email sending failed: {str(e)}")