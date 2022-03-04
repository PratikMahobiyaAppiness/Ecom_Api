from rest_framework import serializers
from . import models

class CoupenSerializer(serializers.ModelSerializer):
	class Meta:
		model 	= models.Coupon
		fields 	= '__all__'