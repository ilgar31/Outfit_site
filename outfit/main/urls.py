from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("goods", views.goods, name='goods'),
    path('login', views.login, name='login'),
    path("registration", views.registration, name='registration'),

]
