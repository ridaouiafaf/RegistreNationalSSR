from django.db import models

# Model de table personne

class Personne(models.Model):

    id_personne = models.IntegerField()
    nom = models.CharField(max_length=45)
    prenom = models.CharField(max_length=45)
    nom = models.CharField(max_length=45)
    date_naiss = models.DateField()
    lieu_naiss = models.CharField(max_length=45)
    cin = models.CharField(max_length=45)
    nationalite = models.CharField(max_length=45)
    adress = models.CharField(max_length=45)
    ville = models.CharField(max_length=45)
    metier = models.CharField(max_length=45)
    etat_civil = models.CharField(max_length=45)
    sexe = models.CharField(max_length=20)
