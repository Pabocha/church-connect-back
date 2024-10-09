from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('annonce', AnnonceViewSet, basename='annonce')
router.register('programme', ProgrammeViewSet, basename='programme')
router.register('affiche',  AfficheViewSet, basename='affiche')

urlpatterns = router.urls