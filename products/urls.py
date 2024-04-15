from django.urls import path

from .views import ProductList, ProductDetail, BrandList, BrandDetail, add_review , get_brand_products, get_product_list
from . import api

urlpatterns = [
    
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>/', BrandDetail.as_view()),


    # Test and train urls :
    path('test/get-brand-products/', get_brand_products),
    path('test/get_product_list/', get_product_list, name='ajax_load_products'),
    
    path('', ProductList.as_view()),
    path('<slug:slug>/', ProductDetail.as_view()),
    path('<slug:slug>/add_review/', add_review),
    
    
    
    # Api Urls :
    path('api/list/', api.ProductListApi.as_view()),
    path('api/list/<int:pk>/', api.ProductDetailApi.as_view()),
    
    path('api/brands/', api.BrandListApi.as_view()),
    path('api/brands/<int:pk>/', api.BrandDetailApi.as_view()),


    
    
]