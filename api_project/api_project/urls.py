"""
URL configuration for api_project project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Include api app URLs here
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')), # Add DRF login/logout views
    path('api/token-auth/', include('rest_framework.authtoken.urls')), # Add token retrieval endpoint
]