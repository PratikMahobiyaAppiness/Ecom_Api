from django.http import JsonResponse
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

from .models import User
from . import serializers

# Create your views here.
# Create Refresh and Access Token (JWT TOKEN's)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# FOR NEW USER REGISTRATION 
class RegisterUserView(APIView):
  def post(self, request):
    serializer = serializers.UserSerializer(data=request.data)
    if not serializer.is_valid():
      return JsonResponse({'status':403, 'errors': serializer.errors})
    user = serializer.save()
    token_obj     = get_tokens_for_user(user)
    return JsonResponse({'status':status.HTTP_201_CREATED, 'data': serializer.data, 'token':token_obj})


class GetProfileView(APIView):
  authentication_classes = [JWTAuthentication,]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    queryset      = User.objects.get(email=request.user)
    serializer    = serializers.UserSerializer(queryset)
    return JsonResponse({'status':status.HTTP_302_FOUND,'data': serializer.data})

  def post(self, request):
    return JsonResponse({'status':status.HTTP_200_OK,'data':'POST TESTED POSITIVE'})

# FOR LOGOUT
class LogoutView(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self, request):
    if self.request.data.get('all'):
        token: OutstandingToken
        for token in OutstandingToken.objects.filter(user=request.user):
          _, _ = BlacklistedToken.objects.get_or_create(token=token)
        return JsonResponse({"status":status.HTTP_205_RESET_CONTENT, "message": "OK, goodbye, all refresh tokens blacklisted"})
    refresh_token = self.request.data.get('refresh_token')
    token = RefreshToken(token=refresh_token)
    token.blacklist()
    return JsonResponse({"status": status.HTTP_205_RESET_CONTENT,"message": "OK, goodbye"})

class ChangePasswordView(APIView):
  authentication_classes = [JWTAuthentication,]
  permission_classes = [IsAuthenticated,]

  def post(self,request):
    serializer = serializers.ChangePasswordSerializer(instance=request.user,data=request.data)
    if not serializer.is_valid():
      return JsonResponse({'status':status.HTTP_304_NOT_MODIFIED, 'errors': serializer.errors})
    user = serializer.save()
    token: OutstandingToken
    for token in OutstandingToken.objects.filter(user=request.user):
      _, _ = BlacklistedToken.objects.get_or_create(token=token)
    token_obj     = get_tokens_for_user(user)
    return JsonResponse({"status":status.HTTP_205_RESET_CONTENT, "message":"Password is Changed", 'token':token_obj})