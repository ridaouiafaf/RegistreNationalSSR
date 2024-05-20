from django.db import models
import uuid

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Facteur(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    religion = models.CharField(max_length=100)
    niv_etud = models.CharField(max_length=100)
    revenu = models.FloatField()
    niv_social = models.CharField(max_length=100)
    impact_norme_culturelle = models.CharField(max_length=100)
    impact_norme_religieuse = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'facteur'

class Enquete(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    doctorant = models.CharField(max_length=100)
    annee_realisation = models.IntegerField()
    id_enquete = models.UUIDField( default=uuid.uuid4, editable=False)

    class Meta:
        managed = False
        db_table = 'enquete'


class Grossesse(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    planification = models.CharField(max_length=100) 
    meth_planification = models.CharField(max_length=100, default="Aucun")  
    envi_enfant = models.CharField(max_length=100)  
    nb_enfant = models.IntegerField()  
    nb_enfant_planifie = models.IntegerField()  
    nb_enfant_nplanifie = models.IntegerField() 
    nb_fausse_couche = models.IntegerField() 
    nb_fausse_couche_intentionnelle = models.IntegerField() 
    nb_enfant_hors_mariage = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'grossesse'

class Doctorant(models.Model):
    ETAT_COMPTE_CHOICES = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    nomComplet = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    role = models.CharField(max_length=20)
    cin = models.CharField(max_length=20, primary_key=True)
    etat_compte = models.CharField(max_length=10, choices=ETAT_COMPTE_CHOICES, default='inactive')

    class Meta:
        managed = False
        db_table = 'doctorant'

class Ist(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    vih_sid = models.CharField(db_column='VIH_SID', max_length=45, blank=True, null=True)  
    syphilis = models.CharField(db_column='SYPHILIS', max_length=45, blank=True, null=True)  
    gonorrhee = models.CharField(max_length=45, blank=True, null=True)
    chlamydiose = models.CharField(max_length=45, blank=True, null=True)
    trichomonase = models.CharField(max_length=45, blank=True, null=True)
    hepatite_b = models.CharField(db_column='hepatite_B', max_length=45, blank=True, null=True) 
    hsv = models.CharField(db_column='HSV', max_length=45, blank=True, null=True)  
    pvh = models.CharField(db_column='PVH', max_length=45, blank=True, null=True)  
    taux_depistoge = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ist'


class Personne(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=45, blank=True, null=True)
    prenom = models.CharField(max_length=45, blank=True, null=True)
    date_naiss = models.DateField(blank=True, null=True)
    cin = models.CharField(max_length=45, blank=True, null=True)
    nationalite = models.CharField(max_length=45, blank=True, null=True)
    adress = models.CharField(max_length=45, blank=True, null=True)
    ville = models.CharField(max_length=45, blank=True, null=True)
    metier = models.CharField(max_length=45, blank=True, null=True)
    etat_civil = models.CharField(max_length=45, blank=True, null=True)
    sexe =  models.CharField(max_length=1, choices=[('H', 'Homme'), ('F', 'Femme')])

    class Meta:
        managed = False
        db_table = 'personne'


class Conscience(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    connaissance = models.CharField(max_length=45, null=True)
    mot_cle_connaissance = models.CharField(max_length=100, null=True)
    utilisation = models.CharField(max_length=45, null=True)
    mot_cle_utilisation = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'conscience'
        

class Pratique(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    connaissance = models.CharField(max_length=45, blank=True, null=True)
    cle_conn = models.CharField(max_length=45, blank=True, null=True)
    consultation = models.CharField(max_length=45, blank=True, null=True)
    question = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pratique'


class PrenatalMaternel(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    acc_serv_prenatal = models.CharField(max_length=100)
    comp_grass = models.CharField(max_length=100)
    desc_comp_gross = models.CharField(max_length=100)
    comp_accouch = models.CharField(max_length=100)
    desc_comp_accouch = models.CharField(max_length=100)
    acc_serv_maternel = models.CharField(max_length=100)
    meth_accouch = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'prenatal_maternel'


class Sr(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    nb_verification_sr = models.IntegerField()
    acc_service_examen = models.CharField(max_length=100)
    problemes_sex = models.CharField(max_length=100)
    qualité_relation_sex = models.CharField(max_length=100)
    demande_soutien = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'sr'


class Violence(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    taux_viol_sex = models.IntegerField(blank=True, null=True)
    agress_sex = models.IntegerField(blank=True, null=True)
    taux_abus_viol_sex = models.IntegerField(blank=True, null=True)
    soutien_psyc = models.CharField(max_length=45, blank=True, null=True)
    type_harcelement_sex = models.CharField(max_length=45, blank=True, null=True)
    taux_harcelement_sex = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'violence'
