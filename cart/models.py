import uuid
from django.db import models
from users.models import User
from store.models import Product

class UserCart(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user 	    			= models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='User')
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Product')
    quantity                = models.PositiveBigIntegerField(verbose_name='Quantity',default=1)
    created_on              = models.DateTimeField(auto_now_add=True)
    modefied_on             = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)

class Order(models.Model):
    bill_no                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name='Bill No.')
    user     				= models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='User Id')
    first_name              = models.CharField(max_length=100,verbose_name='First Name')
    last_name               = models.CharField(max_length=100,verbose_name='Last Name')
    mobile   				= models.BigIntegerField(verbose_name='Contact Number')
    address     			= models.TextField(verbose_name='Address')
    total            		= models.FloatField(verbose_name='Total')
    discount            	= models.FloatField(verbose_name='Discount')
    amount            		= models.FloatField(verbose_name='Amount')
    grand_amount            = models.FloatField(verbose_name='Grand Amount', default=0)
    delivery            	= models.FloatField(verbose_name='Delivery amount')
    order_date              = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.bill_no)

class OrderDetail(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_no                 = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='Bill No')
    item                    = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity     			= models.PositiveBigIntegerField(verbose_name='Quantity')
    mrp                		= models.FloatField(verbose_name='MRP/Quantity')
    total                 	= models.FloatField(verbose_name='Total')
    order_date              = models.DateTimeField(auto_now_add=True)