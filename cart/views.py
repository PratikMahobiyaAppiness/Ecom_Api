import json
from urllib import request
from django.http import JsonResponse
from uritemplate import partial
from . import serializers
from . import models
from rest_framework.views import APIView, status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from . import helper

# Create your views here.
class UserCartView(APIView):
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated]
	def get(self, request):
		user 			= models.User.objects.get(email = request.user)
		cart_helper   = helper.CartHelper(user)
		checkout_details = cart_helper.prepare_cart_for_checkout()

		if not checkout_details:
				return JsonResponse(status=status.HTTP_404_NOT_FOUND,
												data={'error': 'Cart of user is empty.'})

		return JsonResponse({"status":status.HTTP_200_OK, "data":{'checkout_details': checkout_details}})

	def post(self, request):
		user 				= models.User.objects.get(email = request.user)
		product 	  = request.data['product']
		if len(models.UserCart.objects.filter(user=user, product=product)) != 0:
			quantity = models.UserCart.objects.get(user=user, product=product).quantity
			models.UserCart.objects.filter(user=user, product=product).update(quantity = quantity+1)
			queryset = models.UserCart.objects.filter(user = user)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':status.HTTP_202_ACCEPTED, 'count':len(queryset), 'data': serializer.data})
		else:
			price = models.Product.objects.get(id= product).price
			data = {'user': user.id,'product': product, 'price': price}
			serializer = serializers.UserCartSerializer(data=data)
			if not serializer.is_valid():
				return JsonResponse({'status':status.HTTP_304_NOT_MODIFIED, 'errors': serializer.errors})
			serializer.save()
			queryset = models.UserCart.objects.filter(user = user)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':status.HTTP_202_ACCEPTED, 'count':len(queryset), 'data': serializer.data})
	
	def delete(self, request):
		user 			= models.User.objects.get(email = request.user)
		product 	  = request.data['product']
		models.UserCart.objects.get(user = user, product=product).delete()
		queryset = models.UserCart.objects.filter(user = user)
		serializer = serializers.UserCartSerializer(queryset, many=True)
		return JsonResponse({'status':status.HTTP_200_OK, 'count':len(queryset), 'data': serializer.data})

	def put(self, request):
		user 			= models.User.objects.get(email = request.user)
		product 	  = request.data['product']
		quantity = models.UserCart.objects.get(user=user, product=product).quantity
		if quantity == 1:
			models.UserCart.objects.get(user = user, product=product).delete()
			queryset = models.UserCart.objects.filter(user = user)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':status.HTTP_202_ACCEPTED, 'count':len(queryset), 'data': serializer.data})
		else:
			models.UserCart.objects.filter(user=user, product=product).update(quantity = quantity-1)
			queryset = models.UserCart.objects.filter(user = user)
			serializer = serializers.UserCartSerializer(queryset, many=True)
			return JsonResponse({'status':status.HTTP_202_ACCEPTED, 'count':len(queryset), 'data': serializer.data})

class OrderView(ModelViewSet):
	authentication_classes = [JWTAuthentication,]
	permission_classes = [IsAuthenticated]

	def OrderList(self, request):
		user 			= models.User.objects.get(email = request.user)
		queryset = models.Order.objects.filter(user = user).order_by('-order_date')
		serializer = serializers.OrderSerializer(queryset, many=True)
		return JsonResponse({'status':status.HTTP_302_FOUND, 'count':len(queryset), 'data': serializer.data})

	def PlaceOrder(self, request):
		user 				= models.User.objects.get(email = request.user)
		ord_data = {'user':user.id,
								'first_name':request.data['first_name'],
								'last_name':request.data['last_name'],
								'mobile':request.data['mobile'],
								'address':request.data['address'],
								'total':request.data['data']['total'][0]['total_price'],
								'discount':request.data['data']['total'][0]['total_discount'],
								'amount':request.data['data']['amount'][0]['total_amount'],
								'delivery':request.data['data']['amount'][0]['delivery_cost'],
								'grand_amount':request.data['data']['amount'][0]['total_amount'] + request.data['data']['amount'][0]['delivery_cost']
							}
		Ord_Serializer = serializers.OrderSerializer(data=ord_data)
		if not Ord_Serializer.is_valid():
			return JsonResponse({'status':status.HTTP_304_NOT_MODIFIED, 'errors': Ord_Serializer.errors})
		Ord_Serializer.save()
		for product in request.data['data']['products']:
			product_detail = models.Product.objects.get(id = product["product_id"])
			ord_det_data = {'bill_no':Ord_Serializer.data['bill_no'],
											'item':product_detail.id,
											'quantity':product['quantity'],
											'mrp':product_detail.price,
											'total':product_detail.price * product['quantity']
										}
			Ord_Det_serializer = serializers.OrderDetailSerializer(data=ord_det_data)
			if not Ord_Det_serializer.is_valid():
				return JsonResponse({'status':status.HTTP_304_NOT_MODIFIED, 'errors': Ord_Det_serializer.errors})
			Ord_Det_serializer.save()
		ord_data['bill_no'] = Ord_Serializer.data['bill_no']
		ord_data['order_date'] = Ord_Serializer.data['order_date']
		models.UserCart.objects.filter(user = user).delete()
		return JsonResponse({'status':status.HTTP_202_ACCEPTED, 'data': ord_data, 'message':'Order is Placed.'})
	
	def OrderDetail(self, request):
		order = models.Order.objects.get(bill_no = request.data['bill_no'])
		order_serializer = serializers.OrderSerializer(order)
		order_detail = models.OrderDetail.objects.filter(bill_no = request.data['bill_no'])
		ord_det_serializer = serializers.OrderDetailSerializer(order_detail, many=True)
		return JsonResponse({'status':status.HTTP_302_FOUND, 'data': {"orderdetail":order_serializer.data, "products":ord_det_serializer.data}})
