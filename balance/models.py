from django.db import models

from django.urls import reverse


# Create your models here.
class User(models.Model):
    # author = models.ForeignKey('auth.User')
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)

class asset(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, max_length=50)
    asset = models.CharField(max_length=50)
    code = models.CharField(max_length=50, null=False)
    quantity = models.IntegerField()








# values = {'asset' : asset, 'stock_code':stock_code, 'quantity':quantity,
#               'cur_price': cur_price, 'first_price':first_price, 'revenue' : revenue, 'asset_sum':asset_sum}