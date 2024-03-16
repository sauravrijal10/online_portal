
from django.contrib import admin
from django.urls import path, include,re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

from .query import query_view, group_by_branch

schema_view = get_schema_view(
    openapi.Info(
        title="MyApp Docs.",
        default_version='v1',
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/country/', include('country.urls')),
    path('api/branch/', include('branch.urls')),
    path('api/user/', include('user.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/invoice/', include('invoice.urls')),
    path('api/payment/', include('payment.urls')),
    path('api/customer_log/', include('customer_log.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/query/', query_view, name="query"),
    path('api/query_branch/', group_by_branch, name="query_branch")

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
