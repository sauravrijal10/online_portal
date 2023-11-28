
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/country/', include('country.urls')),
    path('api/branch/', include('branch.urls')),
    path('api/user/', include('user.urls')),
]
