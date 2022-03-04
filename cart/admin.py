
from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity','created_on','modefied_on')
    list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bill_no','user','first_name','last_name','mobile','address','total','discount','amount','delivery','grand_amount','order_date')
    readonly_fields = ('bill_no','user','first_name','last_name','mobile','address','total','discount','delivery','amount','order_date')
    list_per_page = 10
    search_fields = ['bill_no','user_id']

@admin.register(models.OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('bill_no_id','item','quantity','mrp','total','order_date')
    readonly_fields = ('bill_no','item','quantity','mrp','total','order_date')
    list_per_page = 10
    search_fields = ['item_name']