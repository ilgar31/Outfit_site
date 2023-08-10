from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("goods/<str:text>", views.search_goods, name='search_goods'),
    path("goods", views.goods, name='goods'),
    path('login', views.login_page, name='login'),
    path("registration", views.registration, name='registration'),
    path("profile/<int:pk>", views.profile, name='profile'),
    path('profile/change', views.profile_change, name='profile_change'),
    path("product/<int:pk>", views.product_page, name='product_page'),
    path("delete_search/", views.delete_search, name='delete_search'),
    path("search_page/", views.search_page, name='search_page'),
    path("search/", views.search_results, name='search'),
    path("basket", views.basket, name='basket'),
    path("purchase/thanks/<int:pk>", views.thanks, name='thanks'),
    path("purchase", views.purchase, name='purchase'),
    path("offer/<int:pk>", views.offer, name='offer'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
]
