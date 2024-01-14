from django.urls import path

from .views import UserViewSet, user_login


app_name = "user"

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list', 'post': 'create'}),name="userviewset"),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    # path('activate/<str:uidb64>/<str:token>/', activate_account, name="activate"),
    path('login/', user_login, name="login"),
]