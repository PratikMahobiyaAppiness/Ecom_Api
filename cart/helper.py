from .models import UserCart
from discount import helper

class CartHelper:
    def __init__(self, user):
        self.user = user
        self.cart_base_total_amount = 0
        self.cart_final_total_amount = 0
        self.campaign_discount_amount = 0
        self.coupon_discount_amount = 0
        self.delivery_cost = 50
        self.cart_items = []
        self.discounts = {}
        self.checkout_details = {'products': [], 'total': [], 'amount': []}

    def prepare_cart_for_checkout(self):
        self.cart_items = UserCart.objects.filter(user_id=self.user)

        if not self.cart_items:
            return False

        self.calculate_cart_base_total_amount()
        self.get_delivery_cost()
        self.get_coupon_discounts()
        self.calculate_discount_amounts()
        self.get_total_amount_after_discounts()
        self.prepare_checkout_details()

        return self.checkout_details

    def get_delivery_cost(self):
        self.delivery_cost = 50 # 50 Rs Default Devilery Cost

    def calculate_cart_base_total_amount(self):
        for cart_item in self.cart_items:
            self.cart_base_total_amount += cart_item.product.price * cart_item.quantity

    def get_coupon_discounts(self):
        coupon_helper = helper.CouponHelper(cart_total_amount=self.cart_base_total_amount)
        self.discounts['coupons'] = coupon_helper.get_coupon_discounts()

    def calculate_discount_amounts(self):
        try:
            for discount in self.discounts.get('coupons', []):
                self.coupon_discount_amount = (self.cart_base_total_amount * discount.amount.get('rate')) / 100
        except Exception as e:
            print('Error when trying to calculating discount amounts {0}'.format(str(e)))

    def get_total_amount_after_discounts(self):

        self.cart_final_total_amount = self.cart_base_total_amount - self.coupon_discount_amount

        return self.cart_final_total_amount

    def prepare_checkout_details(self):
        for cart_item in self.cart_items:
            self.checkout_details['products'].append({'category_id': cart_item.product.category.category,
                                                      'category_name': cart_item.product.category.category,
                                                      'product_id': cart_item.product.id,
                                                      'product_name': cart_item.product.title,
                                                      'quantity': cart_item.quantity,
                                                      'unit_price': cart_item.product.price})

        self.checkout_details['total'].append({'total_price': self.cart_base_total_amount,
                                               'total_discount': self.coupon_discount_amount})

        self.checkout_details['amount'].append({'total_amount': self.cart_final_total_amount,
                                                'delivery_cost': self.delivery_cost})