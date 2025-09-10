from django.views.decorators.csrf import csrf_exempt
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
    print("=== STRIPE WEBHOOK CALLED ===")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.META)}")
    
    payload = request.body
    print(f"Payload length: {len(payload)}")
    
    if 'HTTP_STRIPE_SIGNATURE' not in request.META:
        print("❌ No Stripe signature header found!")
        return HttpResponse(status=400)
    
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print(f"Signature header: {sig_header[:50]}...")

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
    
    
    print(f"📥 Event type: {event.type}")
    
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        print("✅ PaymentIntent was successful!")
        
        # Extract transaction_id from metadata
        if 'transaction' in payment_intent.metadata:
            transaction_id = payment_intent.metadata['transaction']
            print(f"Processing transaction ID: {transaction_id}")
            try:
                make_order(transaction_id)
                print(f"Order created successfully for transaction {transaction_id}")
            except Exception as e:
                print(f"Error creating order for transaction {transaction_id}: {str(e)}")
                return HttpResponse(status=500)
        else:
            print("No transaction metadata found in payment intent")
            return HttpResponse(status=400)
            
    elif event.type == 'charge.succeeded':
        charge = event.data.object
        print("✅ Charge was successful!")
        
        # Get payment intent ID from charge and fetch the payment intent
        payment_intent_id = charge.payment_intent
        print(f"Payment Intent ID: {payment_intent_id}")
        
        try:
            # Fetch the payment intent to get metadata
            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if 'transaction' in payment_intent.metadata:
                transaction_id = payment_intent.metadata['transaction']
                print(f"Processing transaction ID from charge: {transaction_id}")
                make_order(transaction_id)
                print(f"Order created successfully for transaction {transaction_id}")
            else:
                print("No transaction metadata found in payment intent")
        except Exception as e:
            print(f"Error processing charge.succeeded: {str(e)}")
            return HttpResponse(status=500)
            
    else:
        print(f"⚠️ Unhandled event type: {event.type}")
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
    try:
        transaction = models.Transaction.objects.get(pk=transaction_id)
        transaction.status = models.TransactionStatus.Completed
        transaction.save()
        print(f"Transaction {transaction_id} marked as completed")
        
        order = Order.objects.create(transaction=transaction)
        products = Product.objects.filter(pk__in=transaction.items)
        for product in products:
            order.orderitem_set.create(product=product, price=product.price)
        
        print(f"Order created with {products.count()} products")

        msg_html = render_to_string('emails/order.html', {
            'order': order,
            'products': products
        })

        print(f"Sending email to: {order.transaction.customer_email}")
        send_mail(
            subject="New Order - Your Digital Books",
            html_message=msg_html,
            message=msg_html,
            from_email="no-reply@yourstore.com",
            recipient_list=[order.transaction.customer_email],
            fail_silently=False,
        )
        print("Email sent successfully")
        
    except models.Transaction.DoesNotExist:
        print(f"Transaction {transaction_id} not found")
        raise Exception(f"Transaction {transaction_id} not found")
    except Exception as e:
        print(f"Error in make_order: {str(e)}")
        raise e