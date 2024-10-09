from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('user', MemberView, basename='member')
router.register('group', GroupViewSet, basename='group')

urlpatterns = router.urls