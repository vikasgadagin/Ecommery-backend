from django.urls import include, path
from rest_framework.routers import DefaultRouter

from category.views import CategoryViewSet

router=DefaultRouter()
router.register(r'category',CategoryViewSet)

custommethod1=CategoryViewSet.as_view({'delete':'all_category_delete'})

urlpatterns = [
    path('',include(router.urls)),
    path('alldelete/',custommethod1),

]