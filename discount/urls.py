from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'coupen/', views.CoupenApi.as_view(), name = 'coupen'),
]