from django.shortcuts import render
import africastalking
from rest_framework import viewsets
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer

import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import urlencode, quote_plus
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Initialize Africa's Talking API
africastalking.initialize('sandbox', 'atsk_5deb26df875064c0c1a9e72bf56c5df2646f46614a0465f0c4909cbdb3ba583d3ca7f44a')
sms = africastalking.SMS

# OAuth configuration for Auth0
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# Authentication views
def login(request):
    return oauth.auth0.authorize_redirect(request, request.build_absolute_uri(reverse("callback")))

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {"returnTo": request.build_absolute_uri(reverse("index")), "client_id": settings.AUTH0_CLIENT_ID},
            quote_via=quote_plus,
        )
    )

def index(request):
    customers = Customer.objects.all().order_by('-id')[:10]  # Get last 10 customers
    orders = Order.objects.all().order_by('-order_time')[:10]  # Get last 10 orders
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
            "customers": customers,
            "orders": orders,
        },
    )


# ViewSets for Customer and Order
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        customer = order.customer
        message = f"Hi {customer.name}, your order for {order.item} worth ${order.amount} has been received. Thank you!"
        self.send_sms(customer.phone_number, message)

    def send_sms(self, recipient, message):
        try:
            response = sms.send(message, [recipient])
            print(f"SMS sent successfully: {response}")
        except Exception as e:
            print(f"Error while sending SMS: {e}")

# Delivery report callback
@csrf_exempt
def delivery_reports(request):
    if request.method == 'POST':
        print(f"Raw request body: {request.body}")  # Log the raw body
        try:
            data = json.loads(request.body)
            print(f"Delivery report response: {data}")
            return JsonResponse({'message': 'Delivery report received'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

