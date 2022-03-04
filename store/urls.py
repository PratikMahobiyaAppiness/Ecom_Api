from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'product/', views.ProductView.as_view(), name = 'products'),
    path(r'category/', views.ProductCategoryView, name = 'products_category'),
    path(r'category_filter/', views.ProductCategoryFilterView, name = 'products_category_filter'),
    path(r'search/', views.ProductSearchView.as_view(), name = 'product_search'),
    path(r'single_product/', views.SingleProductView, name = 'single_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)