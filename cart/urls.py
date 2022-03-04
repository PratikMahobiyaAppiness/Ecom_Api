from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'usercart/', views.UserCartView.as_view(), name = 'user_cart'),
    path(r'orders/', views.OrderView.as_view({'get': 'OrderList'})),
    path(r'placeorder/', views.OrderView.as_view({'post': 'PlaceOrder'})),
    path(r'orderdetail/', views.OrderView.as_view({ 'get' : 'OrderDetail'})),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)