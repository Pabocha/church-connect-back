from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

frequence_choices = [
    ('jours', 'tous les jours'),
    ('semaines', 'toutes les semaines'),
    ('mois', 'tous les mois')
]

list_day_for_weeks_choices = [
    ('Lun', 'Lundi'),
    ('Mar', 'Mardi'),
    ('Mer', 'Mercredi'),
    ('Jeu', 'Jeudi'),
    ('Ven', 'Vendredi'),
    ('Sam', 'Samedi'),
    ('Dim', 'Dimanche')
]

repete_envent_choices = [
    ("Toujours", "Toujours"),
    ("until", "jusqu'à une certaine date")
]
repete_month_choices = [
    ('same_day', 'Le même jour chaque mois'),
    ('first_day', 'Tous les premiers jours du jour choisi')
]

type_programme_choices = [
    ('habituel', 'Programme habituel'),
    ('special', 'Programme spécial')
]

class DayOfWeek(models.Model):
    abbreviation = models.CharField(max_length=3)
    day = models.CharField(max_length=10)

    def __str__(self):
        return self.day


class Programmes(models.Model):
    titre = models.CharField(max_length=255)
    lieu = models.CharField(max_length=255, null=True, blank=True)
    type_programme = models.CharField(max_length=255, choices=type_programme_choices, default='habituel')
    message = models.TextField(null=True, blank=True)
    begin_date = models.DateField()
    end_date = models.DateField()
    begin_time = models.TimeField(null=True, blank=True)    
    end_time = models.TimeField(null=True, blank=True)  
    frequency = models.CharField(max_length=255, choices=frequence_choices, null=True, blank=True)  
    day_of_weeks = models.ManyToManyField(DayOfWeek,  blank=True)
    repete_event_month = models.CharField(max_length=255, choices=repete_month_choices, null=True, blank=True)
    deadline_repet_event = models.CharField(max_length=255, choices=repete_envent_choices, null=True, blank=True)
    date_until = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="", null=True, blank=True)

    class Meta:
        verbose_name = ('Programme Spécial')
        verbose_name_plural = ('Programmes Spéciaux')

    def __str__(self):
        return self.titre  

class Annonces(models.Model):

    Annonces = [
        ('gn', 'general'),
        ('bt', 'bapteme'),
        ('mg', 'mariage'),
        ('st', 'soutenance'),
        ('ev', 'evangelisation')
    ]

    titre = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    type_announce = models.CharField(max_length=255, choices=Annonces, default="gn")
    lieu = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_view = models.BooleanField(default=True)

    class Meta:
        verbose_name = ('Annonce')
        verbose_name_plural = ('Annonces')
        ordering = ('date_added',)

    def __str__(self):
        return self.titre  
    
class Affiches(models.Model):
    image = models.ImageField(upload_to='')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    is_view = models.BooleanField(default=True)


class Notifications(models.Model):

    CHOICES = [
        ('programme', 'Programme'),
        ('annonce', 'Annonce')
    ]

    title = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    type_notif = models.CharField(max_length=255, choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    annonce = models.ForeignKey(Annonces, on_delete=models.CASCADE, null=True, blank=True)
    programme = models.ForeignKey(Programmes, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)