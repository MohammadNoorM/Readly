from django.urls import path
from checkout import views
from checkout import webhooks

urlpatterns = [
    path('stripe/config/', views.stripe_config, name='checkout.stripe.config'),
    path('stripe', views.stripe_transaction, name='checkout.stripe'),
    path('paypal', views.paypal_transaction, name='checkout.paypal'),
    path('stripe/webhook', webhooks.stripe_webhook),
]

