from django.urls import path

from .views import ProductList, ProductDetail, BrandList, BrandDetail
from . import api

urlpatterns = [
    
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>/', BrandDetail.as_view()),
    
    path('', ProductList.as_view()),
    path('<slug:slug>/', ProductDetail.as_view()),
    
    
    
    # Api Urls :
    path('api/list/', api.ProductListApi.as_view()),
    path('api/list/<int:pk>/', api.ProductDetailApi.as_view()),
    
    path('api/list/brands/', api.BrandListApi.as_view()),
    path('api/list/brands/<int:pk>/', api.BrandDetailApi.as_view()),
    
]