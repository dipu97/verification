from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('',include('products.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns= urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)