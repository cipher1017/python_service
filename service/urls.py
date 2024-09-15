from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
from . import views


urlpatterns = [
    path('', include(router.urls)),
    path("index", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),

]