from django.test import TestCase
from rest_framework.test import APIClient
from .models import Customer, Order

class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        # POST request to create a new customer
        response = self.client.post('/api/customers/', {
            'name': 'David',
            'address': '123 Main Street',
            'phone_number': '123-456-7890'
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_order(self):
        # customer to associate with the order
        customer = Customer.objects.create(
            name="David",
            address="123 Main Street",
            phone_number="+254748272022"
        )
        # POST request to create a new order for the customer
        response = self.client.post('/api/orders/', {
            'customer': customer.id,
            'item': 'Bag',
            'amount': 2300.50
        }, format='json')
        self.assertEqual(response.status_code, 201)
