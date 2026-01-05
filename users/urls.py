from django.urls import include,path
from rest_framework.routers import DefaultRouter

from users.views import UsersViewSet

router =DefaultRouter()
router.register('users',UsersViewSet)
custommethod1=UsersViewSet.as_view({'delete':'all_delete_users'})

urlpatterns = [

    path('',include(router.urls)),
    path('delete/',custommethod1),

]