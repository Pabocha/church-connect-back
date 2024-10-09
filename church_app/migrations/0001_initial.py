# Generated by Django 5.0.7 on 2024-09-04 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Annonces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
                ('type_announce', models.CharField(choices=[('gn', 'general'), ('bt', 'bapteme'), ('mg', 'mariage'), ('st', 'soutenance'), ('ev', 'evangelisation')], default='gn', max_length=255)),
                ('lieu', models.CharField(blank=True, max_length=255, null=True)),
                ('day_time', models.DateTimeField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Annonce',
                'verbose_name_plural': 'Annonces',
                'ordering': ('date_added',),
            },
        ),
        migrations.CreateModel(
            name='DayOfWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=3)),
                ('day', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Programmes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('lieu', models.CharField(blank=True, max_length=255, null=True)),
                ('type_programme', models.CharField(choices=[('habituel', 'Programme habituel'), ('special', 'Programme spécial')], default='habituel', max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField()),
                ('begin_time_of_day', models.TimeField(blank=True, null=True)),
                ('end_time_of_day', models.TimeField(blank=True, null=True)),
                ('frequency', models.CharField(blank=True, choices=[('jours', 'tous les jours'), ('semaines', 'toutes les semaines'), ('mois', 'tous les mois')], max_length=255, null=True)),
                ('repete_event', models.CharField(blank=True, choices=[('same', 'Le même jour chaque mois'), ('first_day', 'Tous les premiers jours du jour choisi')], max_length=255, null=True)),
                ('date_until', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('day_of_weeks', models.ManyToManyField(blank=True, null=True, to='church_app.dayofweek')),
            ],
            options={
                'verbose_name': 'Programme Spécial',
                'verbose_name_plural': 'Programmes Spéciaux',
            },
        ),
    ]
