from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path("register/", views.register, name="register"),
    path("login/", views.login_page, name="login"),
    path("cart/", views.cart_page, name="cart"),
    path("fav", views.fav_page, name="fav"),
    path("favviewpage/", views.favviewpage, name="favviewpage"),
    path("logout/", views.logout_page, name="logout"),
    path("collections/", views.collections, name="collections"),
    path("collections/<str:name>", views.collectionsView, name="collections"),
    path("collections/<str:cname>/<str:pname>", views.product_detail, name="product_detail"),
    path("addtocart", views.add_to_cart, name="addtocart"),
    path("remove_cart/<str:cid>", views.remove_cart, name="remove_cart"),
    path("remove_fav/<str:cid>", views.remove_fav, name="remove_fav"),
]   
