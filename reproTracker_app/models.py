# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    religion = models.CharField(max_length=45, blank=True, null=True)
    niveau_etud = models.CharField(max_length=45, blank=True, null=True)
    statut_socio_eco = models.CharField(max_length=45, blank=True, null=True)
    impact_vie_sex = models.CharField(max_length=45, blank=True, null=True)
    impact_norm_cult = models.CharField(max_length=45, blank=True, null=True)
    impact_norm_relig = models.CharField(max_length=45, blank=True, null=True)
    satis_sex = models.CharField(max_length=45, blank=True, null=True)
    qualite_sex = models.CharField(max_length=45, blank=True, null=True)
    dem_soutien = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'facteur'


class General(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    docteur = models.CharField(max_length=45, blank=True, null=True)
    ann_realise = models.DateField(blank=True, null=True)
    id_enq = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'general'


class Grossesse(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    meth_plan = models.CharField(max_length=45, blank=True, null=True)
    mpf = models.CharField(db_column='MPF', max_length=45, blank=True, null=True)  # Field name made lowercase.
    desir_enf_plan = models.CharField(max_length=45, blank=True, null=True)
    nbr_enf_plan = models.IntegerField(blank=True, null=True)
    nbr_enf_nplan = models.IntegerField(blank=True, null=True)
    nbr_enf_t = models.IntegerField(blank=True, null=True)
    nbr_avort_desir = models.IntegerField(blank=True, null=True)
    nbr_avot_ndesir = models.IntegerField(blank=True, null=True)
    nbr_enf_hors_m = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grossesse'


class Ist(models.Model):
    id_personne = models.CharField(primary_key=True, max_length=45)
    vih_sid = models.CharField(db_column='VIH/SID', max_length=45, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    syphilis = models.CharField(db_column='SYPHILIS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    gonorrhÚe = models.CharField(max_length=45, blank=True, null=True)
    chlamydiose = models.CharField(max_length=45, blank=True, null=True)
    trichomonase = models.CharField(max_length=45, blank=True, null=True)
    hepatite_b = models.CharField(db_column='hepatite_B', max_length=45, blank=True, null=True)  # Field name made lowercase.
    hsv = models.CharField(db_column='HSV', max_length=45, blank=True, null=True)  # Field name made lowercase.
    pvh = models.CharField(db_column='PVH', max_length=45, blank=True, null=True)  # Field name made lowercase.
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
    sexe = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personne'


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
    acc_serv_prenatal = models.CharField(max_length=45, blank=True, null=True)
    comp_grass = models.CharField(max_length=45, blank=True, null=True)
    comp_accouch = models.CharField(max_length=45, blank=True, null=True)
    util_sm = models.CharField(db_column='util_SM', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prenatal_maternel'


class Sr(models.Model):
    id_persone = models.IntegerField(primary_key=True)
    sante_org_genitaux = models.CharField(max_length=45, blank=True, null=True)
    acc_serv_sr = models.CharField(max_length=45, blank=True, null=True)
    prob_impuissance = models.CharField(max_length=45, blank=True, null=True)
    prob_frigidite_sex = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sr'


class Violence(models.Model):
    id_personne = models.IntegerField(primary_key=True)
    violence_sex = models.CharField(max_length=45, blank=True, null=True)
    taux_viol_sex = models.FloatField(blank=True, null=True)
    abus_viol_sex = models.CharField(max_length=45, blank=True, null=True)
    taux_abus_viol_sex = models.FloatField(blank=True, null=True)
    soutien_psyc = models.CharField(max_length=45, blank=True, null=True)
    harcelement_verbal = models.CharField(max_length=45, blank=True, null=True)
    nbr_harcel_verbal = models.IntegerField(blank=True, null=True)
    harcelement_n_verbal = models.CharField(max_length=45, blank=True, null=True)
    nbr_harcel_n_verb = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'violence'
