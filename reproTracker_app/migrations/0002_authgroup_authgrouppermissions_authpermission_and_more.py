# Generated by Django 5.0.4 on 2024-04-28 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reproTracker_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Facteur',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('religion', models.CharField(blank=True, max_length=45, null=True)),
                ('niveau_etud', models.CharField(blank=True, max_length=45, null=True)),
                ('statut_socio_eco', models.CharField(blank=True, max_length=45, null=True)),
                ('impact_vie_sex', models.CharField(blank=True, max_length=45, null=True)),
                ('impact_norm_cult', models.CharField(blank=True, max_length=45, null=True)),
                ('impact_norm_relig', models.CharField(blank=True, max_length=45, null=True)),
                ('satis_sex', models.CharField(blank=True, max_length=45, null=True)),
                ('qualite_sex', models.CharField(blank=True, max_length=45, null=True)),
                ('dem_soutien', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'facteur',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='General',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('docteur', models.CharField(blank=True, max_length=45, null=True)),
                ('ann_realise', models.DateField(blank=True, null=True)),
                ('id_enq', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'general',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Grossesse',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('meth_plan', models.CharField(blank=True, max_length=45, null=True)),
                ('mpf', models.CharField(blank=True, db_column='MPF', max_length=45, null=True)),
                ('desir_enf_plan', models.CharField(blank=True, max_length=45, null=True)),
                ('nbr_enf_plan', models.IntegerField(blank=True, null=True)),
                ('nbr_enf_nplan', models.IntegerField(blank=True, null=True)),
                ('nbr_enf_t', models.IntegerField(blank=True, null=True)),
                ('nbr_avort_desir', models.IntegerField(blank=True, null=True)),
                ('nbr_avot_ndesir', models.IntegerField(blank=True, null=True)),
                ('nbr_enf_hors_m', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'grossesse',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Ist',
            fields=[
                ('id_personne', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('vih_sid', models.CharField(blank=True, db_column='VIH/SID', max_length=45, null=True)),
                ('syphilis', models.CharField(blank=True, db_column='SYPHILIS', max_length=45, null=True)),
                ('gonorrhÚe', models.CharField(blank=True, max_length=45, null=True)),
                ('chlamydiose', models.CharField(blank=True, max_length=45, null=True)),
                ('trichomonase', models.CharField(blank=True, max_length=45, null=True)),
                ('hepatite_b', models.CharField(blank=True, db_column='hepatite_B', max_length=45, null=True)),
                ('hsv', models.CharField(blank=True, db_column='HSV', max_length=45, null=True)),
                ('pvh', models.CharField(blank=True, db_column='PVH', max_length=45, null=True)),
                ('taux_depistoge', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ist',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pratique',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('connaissance', models.CharField(blank=True, max_length=45, null=True)),
                ('cle_conn', models.CharField(blank=True, max_length=45, null=True)),
                ('consultation', models.CharField(blank=True, max_length=45, null=True)),
                ('question', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'pratique',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PrenatalMaternel',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('acc_serv_prenatal', models.CharField(blank=True, max_length=45, null=True)),
                ('comp_grass', models.CharField(blank=True, max_length=45, null=True)),
                ('comp_accouch', models.CharField(blank=True, max_length=45, null=True)),
                ('util_sm', models.CharField(blank=True, db_column='util_SM', max_length=45, null=True)),
            ],
            options={
                'db_table': 'prenatal_maternel',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sr',
            fields=[
                ('id_persone', models.IntegerField(primary_key=True, serialize=False)),
                ('sante_org_genitaux', models.CharField(blank=True, max_length=45, null=True)),
                ('acc_serv_sr', models.CharField(blank=True, max_length=45, null=True)),
                ('prob_impuissance', models.CharField(blank=True, max_length=45, null=True)),
                ('prob_frigidite_sex', models.CharField(blank=True, max_length=45, null=True)),
            ],
            options={
                'db_table': 'sr',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Violence',
            fields=[
                ('id_personne', models.IntegerField(primary_key=True, serialize=False)),
                ('violence_sex', models.CharField(blank=True, max_length=45, null=True)),
                ('taux_viol_sex', models.FloatField(blank=True, null=True)),
                ('abus_viol_sex', models.CharField(blank=True, max_length=45, null=True)),
                ('taux_abus_viol_sex', models.FloatField(blank=True, null=True)),
                ('soutien_psyc', models.CharField(blank=True, max_length=45, null=True)),
                ('harcelement_verbal', models.CharField(blank=True, max_length=45, null=True)),
                ('nbr_harcel_verbal', models.IntegerField(blank=True, null=True)),
                ('harcelement_n_verbal', models.CharField(blank=True, max_length=45, null=True)),
                ('nbr_harcel_n_verb', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'violence',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='personne',
            options={'managed': False},
        ),
    ]
