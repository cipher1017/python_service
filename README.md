Simple Python Service
This project is a simple Python-based service that provides REST APIs for managing customers and orders. It also integrates authentication using OpenID Connect with Auth0 and sends SMS notifications to customers via Africa's Talking when new orders are created. The project is deployed on Heroku and follows a CI/CD pipeline using CircleCI.

Features
    REST API for Customers and Orders: Create, view, and manage customers and orders.
    Authentication: OpenID Connect (OIDC) via Auth0.
    SMS Notifications: Sends SMS alerts using Africa's Talking when an order is placed.
    CI/CD Integration: Continuous integration and deployment using CircleCI.
    Deployed on Heroku.

API Endpoints
    Customers API:
        GET /api/customers/ - Get all customers
        POST /api/customers/ - Create a new customer
    Orders API:
        GET /api/orders/ - Get all orders
        POST /api/orders/ - Create a new order
Authentication
    Authentication is implemented using Auth0 via OpenID Connect. To log in, use the login link, and for logout, redirect to the logout URL.

Allowed Callback URLs:
    Login: https://pythonservice-e03e4a635c7b.herokuapp.com/callback/
    Logout: https://pythonservice-e03e4a635c7b.herokuapp.com/

Sending SMS
    SMS notifications are sent when an order is placed, notifying the customer of their order details. The Africa’s Talking API is used for this purpose.

Installation
To run this project locally:

Clone the repository:

bash
Copy code
git clone https://github.com/cipher1017/python_service.git
cd python_service
Create and activate a virtual environment:
    python3 -m venv venv
    source venv/bin/activate
Install dependencies:
    pip install -r requirements.txt

Set up environment variables in a .env file:
    AUTH0_CLIENT_ID=your_auth0_client_id
    AUTH0_CLIENT_SECRET=your_auth0_client_secret
    AUTH0_DOMAIN=your_auth0_domain
    
Run migrations and start the server:
    python manage.py migrate
    python manage.py runserver

Running Tests
    To run unit tests with coverage:
    python manage.py test

CI/CD Pipeline
    CircleCI is used for continuous integration and deployment.
    Heroku is the deployment platform.

CI/CD Pipeline is configured to:
    Run unit tests.
    Deploy to Heroku via CircleCI after successful tests.

Deployment
    The project is deployed on Heroku. You can access it here:
    App URL: https://pythonservice-e03e4a635c7b.herokuapp.com/

Technology Stack
    Backend: Python, Django, Django REST Framework
    Database: PostgreSQL
    Containerization: Heroku
    CI/CD: CircleCI
    SMS Integration: Africa's Talking
    Authentication: Auth0 (OpenID Connect)