from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group 
from django.contrib.auth import authenticate
from rest_framework import exceptions

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email_or_phone = attrs.get("email")
        password = attrs.get("password")

        # Assurez-vous de trouver l'utilisateur soit par email soit par téléphone
        user = None
        if '@' in email_or_phone:
            # Il semble être un email
            user = authenticate(username=email_or_phone, password=password)
        else:
            # Il semble être un numéro de téléphone
            user = authenticate(username=email_or_phone, password=password)
            


        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,  # équivalent de 'is_admin'
            'is_active': user.is_active,
            'roles': [group.name for group in user.groups.all()] if user.groups.exists() else ['user'],
        }

        return data


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'profession', 'image', 'latitude', 'longitude')

    
class MemberDetailSerializer(serializers.Serializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    image = serializers.ImageField(read_only=True)



class GroupRetreiveSerializer(serializers.ModelSerializer):
    user_groups = MemberSerializer(many=True, read_only=True)
    # user_groups = serializers.StringRelatedField(many=True)
    image = serializers.ImageField(source='group_profile.image', read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'user_groups', 'image')


class GroupSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Group
        fields = ('id', 'name', 'image')

