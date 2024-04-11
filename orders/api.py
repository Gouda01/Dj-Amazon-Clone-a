from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import datetime

from .models import Cart, CartDetail, Order, OrderDetail, Coupon
from products.models import Product
from settings.models import DeliveryFee
from accounts.models import Address
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

                return Response({'message':'Coupon was applied successfully'}, status=status.HTTP_200_OK)
            
            else :
                return Response({'message':'Coupon is invalid or expires'})
            
        return Response({'message':'Coupon not found'})




class CreateOrderAPI(generics.GenericAPIView):
    
    def post(self,request,*args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        code = request.data['payment_code']
        address = request.data['address_id']

        cart = Cart.objects.get(user=user, status='Inprogress')
        cart_detail = CartDetail.objects.filter(cart=cart)
        user_address = Address.objects.get(id=address)

        # cart : order  | cart_detail : order_detail
        new_order = Order.objects.create(
            user = user,
            status = 'Recieved',
            code = code,
            delivery_address = user_address,
            coupon = cart.coupon,
            total_with_coupon = cart.total_with_coupon,
            total = cart.cart_total
        )

        # Order detail
        for item in cart_detail:
            product = Product.objects.get(id=item.product.id)
            OrderDetail.objects.create(
                order = new_order,
                product = product,
                quantity = item.quantity,
                price = product.price,
                total = round(item.quantity * product.price , 2)
            )
            product.quantity -= item.quantity
            product.save()
        
        # Close Cart
        cart.status = 'Completed'

        # Send Email 
        #

        return Response({'message':'Order was created successfully'},status=status.HTTP_201_CREATED)


class CartCreateUpdateDeleteAPI(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs) :
        user = User.objects.get(username=self.kwargs['username'])
        cart , created = Cart.objects.get_or_create(user=user, status='Inprogress')
        data = serializers.CartSerializer(cart).data

        return Response({'cart':data})

    def post(self, request, *args, **kwargs) :
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id= request.data['product_id'])
        quantity = int(request.POST['quantity'])

        cart = Cart.objects.get(user=user, status='Inprogress')
        cart_detail , created = CartDetail.objects.get_or_create(cart=cart,product=product)

        # if not created :
        #     cart_detail.quantity = cart_detail.quantity + quantity

        cart_detail.quantity = quantity
        cart_detail.total = round(product.price * cart_detail.quantity , 2 )
        cart_detail.save()

        return Response({'message':'Cart was updated successfully'},status=status.HTTP_201_CREATED)


    def delete(self, request, *args, **kwargs) :
        user = User.objects.get(username=self.kwargs['username'])
        # cart = Cart.objects.get(user=user, status='Inprogress')
        product = CartDetail.objects.get(id=request.data['item_id'])
        product.delete()

        return Response({'message':'Product deleted successfully from cart'},status=status.HTTP_202_ACCEPTED)