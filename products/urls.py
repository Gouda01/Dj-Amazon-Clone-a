from django.urls import path

from .views import ProductList, ProductDetail, BrandList, BrandDetail, add_review
from . import api

urlpatterns = [
    
    path('brands/', BrandList.as_view()),
    path('brands/<slug:slug>/', BrandDetail.as_view()),
    
    path('', ProductList.as_view()),
    path('<slug:slug>/', ProductDetail.as_view()),
    path('<slug:slug>/add_review/', add_review),
    
    
    
    # Api Urls :
    path('api/list/', api.ProductListApi.as_view()),
    path('api/list/<int:pk>/', api.ProductDetailApi.as_view()),
    
    path('api/brands/', api.BrandListApi.as_view()),
    path('api/brands/<int:pk>/', api.BrandDetailApi.as_view()),
    
]