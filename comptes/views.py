from rest_framework import status, viewsets, views
from .models import Members
from .serializers import *
from django.contrib.auth.models import Group
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from .models import GroupProfile
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from church_app.permissions import IsStaff

# Create your views here.

def send_email(email, first_name, password, *args, **kwargs):
    subject = "Bienvenue Chez Rehoboth Dakar"
    message = (f"Bien aimée {first_name} Nous vous remerçions d'être passer et vous souhaitons la bienvenue dans notre communauté \n" +
              "Et vous encouragons à bien vouloir installé notre application pour voir les annonces et \n" +
              "programme de l'église \n " +
              f"voici votre mot de passe {password}")
    sender = "Rehoboth <{}>".format(settings.EMAIL_HOST_USER)
    recipient = [email]
    send_mail(
        subject,
        message,
        sender,
        recipient,
        fail_silently= False
    )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer    

class MemberView(viewsets.ModelViewSet):

    serializer_class = MemberSerializer

    def get_queryset(self):
        return Members.objects.all()
    
    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]
    
    def list(self, request, *args, **kwargs):
        if 'page' in request.query_params:
            return super().list(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        password = User.objects.make_random_password()
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.set_password(password)
            user.save()

            first_name = serializer.validated_data.get('first_name')
            email = serializer.validated_data.get('email')
            send_email(email, first_name, password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            errors = e.detail
            if 'email' in errors:
                errors['email'] = ["Un membre avec cet email existe déjà."]
            if 'phone_number' in errors:
                errors['téléphone'] = errors.pop('phone_number')  
                errors['téléphone'] = ["Un membre avec ce téléphone existe déjà."] 
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        
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



class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return GroupRetreiveSerializer
        elif self.action in ['create', 'partial_update']:
            return GroupSerializer
        else:
            return GroupRetreiveSerializer
    def get_permissions(self):
        if self.action in ['destroy' 'create', 'partial_update']:
            return [IsStaff(), IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            image = serializer.validated_data.pop('image', None)
            group = serializer.save()
            user.groups.add(group)
            if image: 
                GroupProfile.objects.create(group=group, image=image)
            return Response({'message' 'Données enregistrés avec succes'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            image = serializer.validated_data.pop('image', None)
            group = serializer.save()
            if image:
                GroupProfile.objects.update_or_create(group=group, defaults={'image': image})
            image_url = None
            if group.group_profile and group.group_profile.image:
                image_url = request.build_absolute_uri(group.group_profile.image.url)

            return Response({'message': 'Données mises à jour avec succès', 'image_url': image_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    
class GestionUserGroup(views.APIView):

    def get_permissions(self):
        # Permissions spécifiques pour l'action 'POST'
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return [IsStaff()]
        
        # Permissions spécifiques pour l'action 'GET'
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        

    def post(self, request, *args, **kwargs):
        users_id = request.data.get('user_id', [])
        group_id = request.data.get('group_id')
        if isinstance(users_id, int):
            users_id = [users_id]

        try:
            users = User.objects.filter(id__in=users_id)
        except User.DoesNotExist:
            return Response({"message": "Ces ou cet utilisateur(s) n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
        
        group = Group.objects.get(id=group_id)
        for user in users:
            if not user.groups.filter(id=group.id).exists():
                user.groups.add(group)
            else:
                return Response({"message": "utilisateur déjà dans le groupe"}, status=status.HTTP_208_ALREADY_REPORTED)

        return Response({"message": "utilisateurs ajouté avec succes"}, status=status.HTTP_200_OK)

    
    def delete(self, request, *args, **kwargs):
        users_id = request.data.get('user_id', [])
        group_id = request.data.get('group_id')
        if isinstance(users_id, int):
            users_id = [users_id]  

        users = User.objects.filter(id__in=users_id)
        group = Group.objects.get(id=group_id)
        for user in users:
            user.groups.remove(group)

        return Response({"message": "l'utilisateur à bien été supprimé du groupe"}, status=status.HTTP_204_NO_CONTENT)

    