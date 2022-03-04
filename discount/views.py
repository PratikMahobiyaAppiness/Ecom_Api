from django.http import JsonResponse
from . import serializers
from . import models
from rest_framework.views import APIView, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CoupenApi(APIView):
  authentication_classes = [JWTAuthentication,]
  permission_classes = [IsAuthenticated]
  def get(self, request):
    queryset = models.Coupon.objects.all()
    serializer = serializers.CoupenSerializer(queryset, many=True)
    return JsonResponse({"status":status.HTTP_200_OK, "data":serializer.data})

  def post(self, request):
    serializer = serializers.CoupenSerializer(data=request.data)
    if not serializer.is_valid():
      return JsonResponse({'status':status.HTTP_304_NOT_MODIFIED, 'errors': serializer.errors})
    serializer.save()
    return JsonResponse({"status":status.HTTP_200_OK, "data":serializer.data})