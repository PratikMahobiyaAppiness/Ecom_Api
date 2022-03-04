from . import models

class AvailableDiscount:
    def __init__(self, discount_type, min_purchased_items, amount):
      self.discount_type = discount_type
      self.amount = amount
      self.min_purchased_items = min_purchased_items

class CouponHelper:

    def __init__(self, cart_total_amount):
      self.cart_total_amount = cart_total_amount
      self.available_discounts = []

    def get_coupon_discounts(self):
      coupon_discounts = models.Coupon.objects.filter(minimum_cart_amount__lte=self.cart_total_amount)

      for coupon_discount in coupon_discounts:
        discount = AvailableDiscount(discount_type='Rate',
                                      min_purchased_items=0,
                                      amount={'rate': coupon_discount.discount_rate,
                                              'amount': None})
        self.available_discounts.append(discount)
      return self.available_discounts