from django.urls import path

from .views import signup, user_active, dashboard

urlpatterns = [
    path('signup',signup),
    path('<str:username>/activate',user_active),

    path('dashboard/',dashboard),
]
