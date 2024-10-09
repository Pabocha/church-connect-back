from rest_framework import serializers
from .models import *

class AnnonceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Annonces
        fields = ('__all__')


class ProgrammeSerializer(serializers.ModelSerializer):
    day_of_weeks = serializers.ListField(
        child=serializers.CharField(),  # Accepter une liste de chaînes
        write_only=True,  # Ce champ sera utilisé uniquement à l'écriture
        required=False
    )
    day_of_weeks_display = serializers.SerializerMethodField(read_only=True, required=False)
    class Meta:
        model = Programmes
        fields = ('__all__')
    def get_day_of_weeks_display(self, obj):
        """Méthode pour renvoyer les jours sous forme lisible"""
        return [day.abbreviation for day in obj.day_of_weeks.all()]
    def create(self, validated_data):
        day_of_weeks_data = validated_data.pop('day_of_weeks', None)  # Extraire les abréviations si présentes
        event = Programmes.objects.create(**validated_data)

        if day_of_weeks_data:  # Vérifier si des jours ont été fournis
            days = DayOfWeek.objects.filter(abbreviation__in=day_of_weeks_data)
            event.day_of_weeks.set(days)  
        return event
    def update(self, instance, validated_data):
        day_of_weeks_data = validated_data.pop('day_of_weeks', None)

        # Mise à jour des autres champs du programme
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Si des jours sont fournis, mettre à jour la relation many-to-many
        if day_of_weeks_data:
            days = DayOfWeek.objects.filter(abbreviation__in=day_of_weeks_data)
            instance.day_of_weeks.set(days)  # Mettre à jour les jours associés
        
        instance.save()  
        return instance

class AfficheSerializer(serializers.ModelSerializer):

    class Meta:
        model = Affiches
        fields = ('__all__')


class NotificationSerializer(serializers.ModelSerializer):
    annonce = AnnonceSerializer(read_only=True)
    programme = ProgrammeSerializer(read_only=True)

    class Meta:
        model = Notifications
        fields = ['id', 'title', 'message', 'type_notif', 'is_read', 'timestamp', 'annonce', 'programme']

class NotificationUpdateSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['id', 'is_read']
