import uuid
from django.db import models

# Create your models here.
class Coupon(models.Model):
  id                    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  minimum_cart_amount   = models.DecimalField(max_digits=10, decimal_places=2, null=False,verbose_name="Mimimun Cart value")
  discount_rate         = models.IntegerField(null=False,verbose_name="Discount %")
  created_at            = models.DateTimeField(auto_now_add=True)
  updated_at            = models.DateTimeField(auto_now=True)
  
  def __str__(self):
      return "{} - {} - {} - {}".format(self.minimum_cart_amount,
                                        self.discount_rate,
                                        self.created_at,
                                        self.updated_at)