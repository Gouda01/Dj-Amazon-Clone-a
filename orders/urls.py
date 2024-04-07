from django.urls import path

from .views import order_list, checkout, add_to_cart
from . import api


urlpatterns = [
    path('', order_list),
    path('checkout/', checkout),
    path('add-to-cart', add_to_cart),



    # Api Urls
    path('api/<str:username>/orders', api.OrderListAPI.as_view()),
    path('api/<str:username>/orders/<int:pk>', api.OrderDetailAPI.as_view()),
    path('api/<str:username>/apply-coupon', api.ApplyCouponAPI.as_view()),
]
