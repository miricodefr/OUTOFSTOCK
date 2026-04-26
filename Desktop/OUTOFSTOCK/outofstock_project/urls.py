"""
URL configuration for outofstock_project project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),   # admin panel
    path('', include('store.urls')),   # all your website pages
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # serve uploaded images