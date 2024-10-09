from django.urls import path
from . import views 

urlpatterns = [
    path('members/', views.GestionUserGroup.as_view()),
]