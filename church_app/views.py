from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from .models import *
from .serializers import *
from rest_framework.exceptions import ValidationError
# from django.utils import timezone
# from datetime import timedelta
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from .permissions import IsStaff


# Create your views here.

class AnnonceViewSet(ModelViewSet):
    serializer_class = AnnonceSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ici, on renvoie toujours les dernières données de la base
        return Annonces.objects.all()
    def get_permissions(self):
        """
        Instancie les permissions pour chaque action.
        """
        if self.action in ['create', 'partial_update', 'destroy']:
            # Applique une permission différente pour la création
            return [IsStaff(), IsAuthenticated()]
        return super().get_permissions()


    def list(self, request, *args, **kwargs):
        # Vérifier si le paramètre 'page' est présent dans la requête
        if 'page' in request.query_params:
            # Si 'page' est présent, utiliser la pagination
            return super().list(request, *args, **kwargs)
        else:
            # Si 'page' n'est pas présent, retourner tous les résultats sans pagination
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e.detail)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RecentAnnonceView(generics.ListAPIView):
    serializer_class = AnnonceSerializer

    def get_queryset(self):
        return Annonces.objects.filter(is_view=True)
    
class AfficheView(generics.ListAPIView):
    serializer_class = AfficheSerializer

    def get_queryset(self):
        return Affiches.objects.filter(is_view=True)



class ProgrammeViewSet(ModelViewSet):
    serializer_class = ProgrammeSerializer
    pagination_class = None

    def get_queryset(self):
        return Programmes.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            # Applique une permission différente pour la création
            return [IsStaff(), IsAuthenticated()]
        return super().get_permissions()

class AfficheViewSet(ModelViewSet): 
    queryset = Affiches.objects.all()
    serializer_class = AfficheSerializer

    def get_permissions(self):
        if self.action in ['create', 'partial_update', 'destroy']:
            return [IsStaff(), IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request, *args, **kwargs):
        user_ids = request.data.get('ids', None)

        if not user_ids:
            return Response({"detail": "No user IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(user_ids, list):
            users_to_delete = User.objects.filter(id__in=user_ids)
        else:
            return Response({"detail": "Invalid data format. Expected a list of IDs."}, status=status.HTTP_400_BAD_REQUEST)

        if not users_to_delete.exists():
            return Response({"detail": "No matching users found."}, status=status.HTTP_404_NOT_FOUND)

        count, _ = users_to_delete.delete()

        return Response({"detail": f"{count} users deleted."}, status=status.HTTP_204_NO_CONTENT)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Notifications.objects.filter(user=self.request.user).order_by('-timestamp')


@api_view(['GET'])
def notification_count(request):
    user = request.user
    count = Notifications.objects.filter(user=user, is_read=False).count()  
    return Response({'count': count})

@api_view(['PATCH'])
def notification_update(request, notification_id):
    user = request.user

    try:
        # On récupère la notification appartenant à l'utilisateur et dont l'ID correspond
        notification = Notifications.objects.get(id=notification_id, user=user)
    except Notifications.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

    # Mise à jour du champ is_read
    notification.is_read = True
    notification.save()

    return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)