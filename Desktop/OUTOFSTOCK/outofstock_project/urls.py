"""
URL configuration for outofstock_project project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # admin panel
    path('', include('store.urls')),   # all your website pages
]
