from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Coupon)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id','minimum_cart_amount','discount_rate','created_at','updated_at')
    list_per_page = 10