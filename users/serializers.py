import email
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models


class UserSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password,])
	class Meta:
		model = models.User
		fields = ('email', 'password', 'password2', 'first_name', 'last_name')
		extra_kwargs = {
					'email'			: {'required': True},
					'password'	: {'required': True},
					'password2'	: {'required': True},
					'first_name': {'required': True},
					'last_name'	: {'required': True}
			}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
				raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def create(self, validated_data):
		user = models.User.objects.create(
				email=validated_data['email'],
				first_name=validated_data['first_name'],
				last_name=validated_data['last_name']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class ChangePasswordSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)
	old_password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = models.User
		fields = ('old_password', 'password', 'password2')
		extra_kwargs = {
				'old_password' 	: {'required': True},
				'password'			: {'required': True},
				'password2'			: {'required': True},
				}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def validate_old_password(self, value):
		user = models.User.objects.get(email=self.instance)
		if not user.check_password(value):
			raise serializers.ValidationError({"old_password": "Old password is not correct"})
		return value

	def update(self, instance, validated_data):
		instance.set_password(validated_data['password'])
		instance.save()
		return instance