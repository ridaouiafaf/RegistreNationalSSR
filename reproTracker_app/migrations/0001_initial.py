# Generated by Django 5.0.4 on 2024-04-23 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_personne', models.IntegerField()),
                ('prenom', models.CharField(max_length=45)),
                ('nom', models.CharField(max_length=45)),
                ('date_naiss', models.DateField()),
                ('lieu_naiss', models.CharField(max_length=45)),
                ('cin', models.CharField(max_length=45)),
                ('nationalite', models.CharField(max_length=45)),
                ('adress', models.CharField(max_length=45)),
                ('ville', models.CharField(max_length=45)),
                ('metier', models.CharField(max_length=45)),
                ('etat_civil', models.CharField(max_length=45)),
                ('sexe', models.CharField(max_length=20)),
            ],
        ),
    ]
