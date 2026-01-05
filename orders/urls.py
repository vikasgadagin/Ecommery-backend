from django.urls import include,path
from rest_framework.routers import DefaultRouter

from orders.views import OrdersViewSet
from users.views import UsersViewSet

router =DefaultRouter()
router.register(r'orders',OrdersViewSet)


urlpatterns = [
    path('',include(router.urls)),
]