from django.urls import path

from .views import order_list, checkout, add_to_cart, process_payment, payment_failed, payment_success
from . import api


urlpatterns = [
    path('', order_list),
    path('checkout/', checkout),
    path('add-to-cart', add_to_cart),

    path('checkout/process-payment', process_payment),
    path('checkout/payment/success', payment_success),
    path('checkout/payment/failed', payment_failed),


    # Api Urls
    path('api/<str:username>/orders', api.OrderListAPI.as_view()),
    path('api/<str:username>/orders/<int:pk>', api.OrderDetailAPI.as_view()),
    path('api/<str:username>/apply-coupon', api.ApplyCouponAPI.as_view()),

    path('api/<str:username>/cart', api.CartCreateUpdateDeleteAPI.as_view()),
    path('api/<str:username>/orders/create', api.CreateOrderAPI.as_view()),

]
