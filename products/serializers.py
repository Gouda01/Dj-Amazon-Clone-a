from rest_framework import serializers

from .models import Product, Brand, Review, ProductImages


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductImages
        fields = ['image']

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta :
        model = Review
        fields = ['user','review','rate','created_at']



class ProductListSerializer(serializers.ModelSerializer) :
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id','name','flag','price','image','sku','subtitle','description','brand','review_count','avg_rate']


class ProductDetailSerializer(serializers.ModelSerializer) :
    brand = serializers.StringRelatedField()
    images = ProductImageSerializer(source='product_image', many=True)
    reviews = ProductReviewSerializer(source='review_product', many=True)

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id','name','flag','price','image','images','sku','subtitle','description','brand','reviews','review_count','avg_rate']

    

    
    
        

class BrandListSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Brand
        fields = '__all__'
        
        
class BrandDetailSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Brand
        fields = '__all__'