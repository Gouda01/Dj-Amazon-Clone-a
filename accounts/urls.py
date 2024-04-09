from django.urls import path

from .views import signup, user_active

urlpatterns = [
    path('signup',signup),
    path('<str:username>/activate',user_active),
]
