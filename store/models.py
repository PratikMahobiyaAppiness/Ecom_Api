import uuid
from django.db import models
from django.utils.html import mark_safe

class ProductCategory(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category 				= models.CharField(max_length=200, unique=True, verbose_name = "Category")
    created_on              = models.DateTimeField(auto_now_add=True)
    modefied_on             = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.category

class Product(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category 			    = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,verbose_name='Category')
    title       			= models.CharField(max_length=100,verbose_name='Title')
    price            		= models.FloatField(verbose_name='Price',default=0)
    description     		= models.TextField(verbose_name='Description')
    img 					= models.ImageField(verbose_name='Image',upload_to ='product_images')
    created_on              = models.DateTimeField(auto_now_add=True)
    modefied_on             = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)
    @property
    def thumbnail_preview(self):
        if self.img:
            return mark_safe('<img src="{}" width="40" height="40" />'.format(self.img.url))
        return "No Image"