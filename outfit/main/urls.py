from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("goods", views.goods, name='goods'),
    path('login', views.login_page, name='login'),
    path("registration", views.registration, name='registration'),
    path("profile", views.profile, name='profile'),
    path('profile/change', views.profile_change, name='profile_change'),
    path("product/<int:pk>", views.product_page, name='product_page'),
    path("search/", views.search_results, name='search'),
    path("add_to_favourites/<int:pk>", views.add_to_favourites, name='add_to_favourites'),
    path("add_to_basket/<int:pk>", views.add_to_basket, name='add_to_basket'),
    path("basket", views.basket, name='basket'),
]
