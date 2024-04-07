from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import datetime

from .models import Cart, CartDetail, Order, OrderDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee
from . import serializers


class OrderListAPI(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super(OrderListAPI, self).get_queryset()
        user = User.objects.get(username=self.kwargs['username'])
        queryset = queryset.filter(user=user)
        return queryset
    
    # def list(self, request, *args, **kwargs):
    #     queryset = super(OrderListAPI, self).get_queryset()
    #     user = User.objects.get(username=self.kwargs['username'])
    #     queryset = queryset.filter(user=user)
    #     data = serializers.OrderSerializer(queryset, many=True).data
    #     return Response({'order':data})


class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()



class ApplyCouponAPI(generics.GenericAPIView) :
    def post(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])   # Get data from url
        coupon = get_object_or_404(Coupon, code=request.data['coupon_code']) # Get data from request body
        delivery_fee = DeliveryFee.objects.last().fee
        cart = Cart.objects.get(user=user, status='Inprogress')

        if coupon and coupon.quantity > 0 :
            today_date = datetime.datetime.today().date()
            if today_date >= coupon.start_date and today_date <= coupon.end_date :
                coupon_value = round(cart.cart_total / 100 * coupon.discount,2)
                sub_total = cart.cart_total - coupon_value
                total = sub_total + delivery_fee

                cart.coupon = coupon
                cart.total_with_coupon = sub_total
                cart.save()

                coupon.quantity -= 1
                coupon.save()

                return Response({'message':'Coupon was applied successfully'})
            
            else :
                return Response({'message':'Coupon is invalid or expires'})
            
        return Response({'message':'Coupon not found'})