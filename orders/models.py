from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Order (models.Model):
    user = models.ForeignKey(User, 'order_user', on_delete=models.SET_NULL, null=True, blank=True)

class OrderDetail(models.Model):
    pass
