from django.urls import path
from . import views 

urlpatterns = [
    path('view-annonce/', views.RecentAnnonceView.as_view(), name='view-annonce'),
    path('view-affiche/', views.AfficheView.as_view(), name='view-affiche'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/count/', views.notification_count, name='notifications_count'),
    path('notifications/<int:notification_id>/update/', views.notification_update, name='notification-update')
]