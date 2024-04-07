from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Cart, CartDetail, Order, OrderDetail
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