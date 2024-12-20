# root/urls.py

from django.contrib import admin
from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from utils.swagger.swagger_views import urlpatterns as swagger_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('api.urls.auth_url'), name='login'),
    path('admin/', admin.site.urls),
    path('categories/', include('api.urls.categories_url')),
    path('clients/', include('api.urls.client_url')),
    path('messages/', include('api.urls.message_url')),
    path('orders/', include('api.urls.order_url')),
    path('order_items/', include('api.urls.order_item_url')),
    path('products/', include('api.urls.product_url')),
    path('users/', include('api.urls.user_url')),
    path('', include(swagger_urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
