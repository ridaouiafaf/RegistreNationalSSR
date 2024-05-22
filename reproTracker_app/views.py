import json, os, re, bcrypt, random, string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib import auth, messages
from django.db import connection,transaction
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.db.models import Count, Q, Max
from django.core.mail import send_mail
from django.conf import settings
from .models import Personne, Pratique, Ist, Grossesse, Facteur, PrenatalMaternel, Violence, Sr 
from .forms import PersonneForm, PratiqueForm, IstForm, GrossesseForm, FacteurForm, PrenatalMaternelForm, ViolenceForm, SrForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import PersonneForm, PratiqueForm, IstForm, GrossesseForm, FacteurForm, PrenatalMaternelForm, ViolenceForm, SrForm
from .models import *
from datetime import datetime
from collections import defaultdict

@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT cin, role, etat_compte, password, nomComplet FROM doctorant WHERE email = %s", [email])
            row = cursor.fetchone()

            if row:
                cin, role, etat_compte, hashed_password, nomComplet = row
                try:
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        if etat_compte == "active":
                            request.session['user_authenticated'] = True
                            request.session['user_cin'] = cin 
                            request.session['user_role'] = role 
                            request.session['user_name'] = nomComplet
                            if role == "responsable":
                                return redirect('index')
                            else:
                                return redirect('index2')
                        else:
                            error_message = "Le compte n'est pas activé. Veuillez attendre l'activation du compte."
                            return render(request, 'login.html', {'error_message': error_message})
                    else:
                        error_message = "Nom d'utilisateur ou mot de passe incorrect."
                        return render(request, 'login.html', {'error_message': error_message})
                except ValueError:
                    error_message = "Erreur de vérification du mot de passe. Veuillez réessayer."
                    return render(request, 'login.html', {'error_message': error_message})
            else:
                error_message = "Le compte n'existe pas. Veuillez créer un compte."
                return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def reset_password(request):
    if request.method == 'POST':
        reset_email = request.POST.get('resetEmail')
        try:
            user = Doctorant.objects.get(email=reset_email)
            new_password = generate_random_password()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE doctorant SET password = %s WHERE email = %s ",[hashed_password, reset_email] )
            send_mail(
                'Réinitialisation de votre mot de passe',
                f'Votre nouveau mot de passe est : {new_password}',
                settings.EMAIL_HOST_USER,
                [reset_email],
                fail_silently=False,
            )
            success_message = "Un email de réinitialisation de mot de passe a été envoyé à votre adresse email."
            return render(request, 'login.html', {'success_message': success_message})
        except Doctorant.DoesNotExist:
            error_message = "Aucun utilisateur trouvé avec cette adresse email."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return redirect('login')

def generate_random_password(length=10):
    """Generate a random password."""
    # You can customize the length or other parameters here if needed
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def username(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    user_name = request.session.get('user_name')  
    context = {
        'user_name': user_name
    }
    return render(request, 'sidebar_doc.html', context)

def inscrire(request):
    if request.method == 'POST':
        nomComplet = request.POST.get('nom_prenom')
        if nomComplet:
            nomComplet = nomComplet.strip().lower()
        email = request.POST.get('email')
        if email:
            email = email.strip().lower()
        password = request.POST.get('passwordInscrire')
        if password:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        telephone = request.POST.get('tele')
        role = request.POST.get('role')
        cin = request.POST.get('cin')
        if cin:
            cin = cin.strip().upper()

        # Vérifiez les doublons
        if Doctorant.objects.filter(email=email).exists():
            duplicate_message = "L'email est déjà existé, essayez de s'authentifier."
            return render(request, 'login.html', {'duplicate_message': duplicate_message})
        
        if Doctorant.objects.filter(cin=cin).exists():
            duplicate_message = "Le CIN est déjà existé, essayez de s'authentifier."
            return render(request, 'login.html', {'duplicate_message': duplicate_message})

        # Créez le nouveau doctorant si aucun doublon n'est trouvé
        doctorant = Doctorant.objects.create(
            nomComplet=nomComplet,
            email=email,
            password=hashed_password,
            telephone=telephone,
            role=role,
            cin=cin
        )
        
        success_message = '''Votre compte est créé avec succès.
                            Veuillez attendre l'activation de votre compte.'''
        return render(request, 'login.html', {'success_message': success_message})
    else:
        return redirect('login')

def validate_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def validate_phone(phone):
    phone_regex = r'^(\+212|00212|0)(6|7)[0-9]{8}$'
    return re.match(phone_regex, phone)



def index(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    
    user_role = request.session.get('user_role')
    
    if user_role != 'responsable':
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM PERSONNE")
        person = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'H'")
        count_h = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'F'")
        count_f = cursor.fetchone()[0]
    
    # for gender by birth year line chart
    selected_year = request.GET.get('year')
    personnes = Personne.objects.all()
    h_ycounts = defaultdict(int)
    f_ycounts = defaultdict(int)
    for personne in personnes:
        if personne.date_naiss:
            year = personne.date_naiss.year
            if personne.sexe == 'H':
                h_ycounts[year] += 1
            elif personne.sexe == 'F':
                f_ycounts[year] += 1
    years = sorted(set(h_ycounts.keys()).union(f_ycounts.keys()))
    homme_data = [h_ycounts[year] for year in years]
    femme_data = [f_ycounts[year] for year in years]
    # Filter data based on selected year
    if selected_year:
        selected_year = int(selected_year)
        if selected_year in years:
            homme_data = [h_ycounts[selected_year]]
            femme_data = [f_ycounts[selected_year]]
            years = [selected_year]

    # les données de graphe pie IST
    vih_sid_count = Ist.objects.filter(vih_sid='oui').count()
    syphilis_count = Ist.objects.filter(syphilis='oui').count()
    gonorrhee_count = Ist.objects.filter(gonorrhee='oui').count()
    chlamydiose_count = Ist.objects.filter(chlamydiose='oui').count()
    trichomonase_count = Ist.objects.filter(trichomonase='oui').count()
    hepatite_b_count = Ist.objects.filter(hepatite_b='oui').count()
    hsv_count = Ist.objects.filter(hsv='oui').count()
    pvh_count = Ist.objects.filter(pvh='oui').count()

    # chart sexual satisfaction X martial status
    selected_status = request.GET.get('marital_status', 'all')
    
    # Filter persons by selected marital status
    if selected_status == 'all':
        personnes = Personne.objects.all()
    else:
        personnes = Personne.objects.filter(etat_civil=selected_status)

    sr_records = Sr.objects.filter(id_personne__in=[p.id_personne for p in personnes])
    combined_data = []

    for personne in personnes:
        sr_record = sr_records.filter(id_personne=personne.id_personne).first()
        if sr_record:
            combined_data.append({
                'etat_civil': personne.etat_civil,
                'qualité_relation_sex': sr_record.qualité_relation_sex,
            })

    # Aggregate the combined data
    data = {}
    for item in combined_data:
        key = (item['etat_civil'], item['qualité_relation_sex'])
        if key not in data:
            data[key] = 0
        data[key] += 1

    # Prepare data for the chart
    marital_status = []
    satisfaction_levels = []
    counts = []

    for key, count in data.items():
        marital_status.append(key[0])
        satisfaction_levels.append(key[1])
        counts.append(count)

    context= {
        'person': person,
        'count_homme': count_h, 
        'count_femme': count_f,
        'personnes': personnes,
        'vih_sid_count': vih_sid_count,
        'syphilis_count': syphilis_count,
        'gonorrhee_count': gonorrhee_count,
        'chlamydiose_count': chlamydiose_count,
        'trichomonase_count': trichomonase_count,
        'hepatite_b_count': hepatite_b_count,
        'hsv_count': hsv_count,
        'pvh_count': pvh_count,
        'years': years,
        'homme_data': homme_data,
        'femme_data': femme_data,
        'selected_year': selected_year,
        'marital_status': marital_status,
        'satisfaction_levels': satisfaction_levels,
        'counts': counts,
        'selected_status': selected_status,
        'all_statuses': Personne.objects.values_list('etat_civil', flat=True).distinct()
    }
    return render(request, 'index.html', context)

def index2(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    user_role = request.session.get('user_role')   
    if user_role != 'doctorant':
        return redirect('login')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM PERSONNE")
        person = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'H'")
        count_h = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'F'")
        count_f = cursor.fetchone()[0]
    
    # for gender by birth year line chart
    selected_year = request.GET.get('year')
    personnes = Personne.objects.all()
    h_ycounts = defaultdict(int)
    f_ycounts = defaultdict(int)
    for personne in personnes:
        if personne.date_naiss:
            year = personne.date_naiss.year
            if personne.sexe == 'H':
                h_ycounts[year] += 1
            elif personne.sexe == 'F':
                f_ycounts[year] += 1
    years = sorted(set(h_ycounts.keys()).union(f_ycounts.keys()))
    homme_data = [h_ycounts[year] for year in years]
    femme_data = [f_ycounts[year] for year in years]
    # Filter data based on selected year
    if selected_year:
        selected_year = int(selected_year)
        if selected_year in years:
            homme_data = [h_ycounts[selected_year]]
            femme_data = [f_ycounts[selected_year]]
            years = [selected_year]

    # les données de graphe pie IST
    vih_sid_count = Ist.objects.filter(vih_sid='oui').count()
    syphilis_count = Ist.objects.filter(syphilis='oui').count()
    gonorrhee_count = Ist.objects.filter(gonorrhee='oui').count()
    chlamydiose_count = Ist.objects.filter(chlamydiose='oui').count()
    trichomonase_count = Ist.objects.filter(trichomonase='oui').count()
    hepatite_b_count = Ist.objects.filter(hepatite_b='oui').count()
    hsv_count = Ist.objects.filter(hsv='oui').count()
    pvh_count = Ist.objects.filter(pvh='oui').count()

    # chart sexual satisfaction X martial status
    selected_status = request.GET.get('marital_status', 'all')
    
    # Filter persons by selected marital status
    if selected_status == 'all':
        personnes = Personne.objects.all()
    else:
        personnes = Personne.objects.filter(etat_civil=selected_status)

    sr_records = Sr.objects.filter(id_personne__in=[p.id_personne for p in personnes])
    combined_data = []

    for personne in personnes:
        sr_record = sr_records.filter(id_personne=personne.id_personne).first()
        if sr_record:
            combined_data.append({
                'etat_civil': personne.etat_civil,
                'qualité_relation_sex': sr_record.qualité_relation_sex,
            })

    # Aggregate the combined data
    data = {}
    for item in combined_data:
        key = (item['etat_civil'], item['qualité_relation_sex'])
        if key not in data:
            data[key] = 0
        data[key] += 1

    # Prepare data for the chart
    marital_status = []
    satisfaction_levels = []
    counts = []

    for key, count in data.items():
        marital_status.append(key[0])
        satisfaction_levels.append(key[1])
        counts.append(count)

    context= {
        'person': person,
        'count_homme': count_h, 
        'count_femme': count_f,
        'personnes': personnes,
        'vih_sid_count': vih_sid_count,
        'syphilis_count': syphilis_count,
        'gonorrhee_count': gonorrhee_count,
        'chlamydiose_count': chlamydiose_count,
        'trichomonase_count': trichomonase_count,
        'hepatite_b_count': hepatite_b_count,
        'hsv_count': hsv_count,
        'pvh_count': pvh_count,
        'years': years,
        'homme_data': homme_data,
        'femme_data': femme_data,
        'selected_year': selected_year,
        'marital_status': marital_status,
        'satisfaction_levels': satisfaction_levels,
        'counts': counts,
        'selected_status': selected_status,
        'all_statuses': Personne.objects.values_list('etat_civil', flat=True).distinct()
    }
    return render(request, 'index2.html', context)

def index3(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    
    user_role = request.session.get('user_role')
    
    if user_role != 'responsable':
        return redirect('login')

    return render(request, 'index3.html')

def enquetes(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    if request.session.get('user_authenticated'):
        current_user_cin = request.session.get('user_cin')

    current_directory = os.path.join(os.path.dirname(__file__), 'templates')
    metiers_path = os.path.join(current_directory, 'métiers.json')
    villes_path = os.path.join(current_directory, 'villes.json')

    with open(villes_path, 'r', encoding='utf-8') as file:
        villes = json.load(file)
    with open(metiers_path, 'r', encoding='utf-8') as file:
        metiers = json.load(file)
    
    return render(request, 'enquetes.html', {
        'villes': villes,
        'metiers': metiers,
        'cin_user':current_user_cin
    })


def compte_active(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'responsable':
        return redirect('login')
    current_user_cin = request.session.get('user_cin')
    if current_user_cin:
        data = Doctorant.objects.filter(etat_compte='active').exclude(cin=current_user_cin)
    else:
        data = Doctorant.objects.filter(etat_compte='active')
    return render(request, 'compte_active.html', {'data': data})

def desactiver_compte(request, cin):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'responsable':
        return redirect('login')
    
    doctorant = get_object_or_404(Doctorant, cin=cin)
    doctorant.etat_compte = 'inactive'
    doctorant.save()
    messages.success(request, f"Le compte avec {cin} est désactivé")
    return redirect('compte_active')

def activer_compte(request, cin):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'responsable':
        return redirect('login')
    doctorant = get_object_or_404(Doctorant, cin=cin)
    doctorant.etat_compte = 'active'
    doctorant.save()
    messages.success(request, f"Le compte avec {cin} est activé")
    return redirect('compte_desactive')

def compte_desactive(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'responsable':
        return redirect('login')
    if request.session.get('user_authenticated'):
        current_user_cin = request.session.get('user_cin')
        if current_user_cin:
            data = Doctorant.objects.filter(etat_compte='inactive').exclude(cin=current_user_cin)
        else:
            data = Doctorant.objects.filter(etat_compte='inactive')
    else:
        data = Doctorant.objects.filter(etat_compte='inactive')
    return render(request, 'compte_desactive.html', {'data': data})

@transaction.atomic
def enquete_soumis(request):
    if request.method == 'POST' :
        try:
            if request.session.get('user_authenticated'):
                current_user_cin = request.session.get('user_cin')
            
            
            # Personne oooooooookkkk
            prenom = request.POST.get('prenom')
            nom = request.POST.get('nom')
            cin = request.POST.get('cin')
            date_naiss = request.POST.get('dateNaissance')
            nationalite = request.POST.get('nationnalite')
            adress = request.POST.get('adresse')
            ville = request.POST.get('ville')
            metier = request.POST.get('metier')
            etat_civil = request.POST.get('etatCivil')
            sexe = request.POST.get('genre')
            personne = Personne.objects.create(
                nom=nom,
                prenom=prenom,
                date_naiss=date_naiss,
                cin=cin,
                nationalite=nationalite,
                adress=adress,
                ville=ville,
                metier=metier,
                etat_civil=etat_civil,
                sexe=sexe
            )
            id_personne = Personne.objects.filter(cin=cin).aggregate(Max('id_personne'))['id_personne__max']

            # Conscience oookkk
            connaissance = request.POST.get('conscience')
            mot_cle_connaissance = request.POST.get('motCleConscience')
            utilisation = request.POST.get('utilisation')
            mot_cle_utilisation = request.POST.get('motCleUtilisation')

            conscience = Conscience.objects.create(
                id_personne=id_personne,
                connaissance=connaissance,
                mot_cle_connaissance=mot_cle_connaissance,
                utilisation=utilisation,
                mot_cle_utilisation=mot_cle_utilisation
            )

            #Ist oooookkkk
            vih_sid = request.POST.get('vih')
            syphilis = request.POST.get('syphilis')
            gonorrhee = request.POST.get('gonorrhee')
            chlamydiose = request.POST.get('chlamydia')
            trichomonase = request.POST.get('trichomonase')
            hepatite_b = request.POST.get('hepatiteB')
            hsv = request.POST.get('hsv2')
            pvh = request.POST.get('hpv')
            taux_depistoge = request.POST.get('ist')

            ist = Ist.objects.create(
                id_personne = id_personne,
                vih_sid = vih_sid,
                syphilis = syphilis,
                gonorrhee = gonorrhee,
                chlamydiose = chlamydiose,
                trichomonase = trichomonase,
                hepatite_b = hepatite_b,
                hsv = hsv,
                pvh = pvh,
                taux_depistoge = taux_depistoge
            )

            #Grossesse  ooooookkkkkk
            planification = request.POST.get('planification') 
            meth_planification = request.POST.get('methode') 
            if meth_planification == '':
                meth_planification="Aucun"
            envi_enfant = request.POST.get('envi_enfant') 
            nb_enfant = request.POST.get('nombre_enfant') 
            nb_enfant_planifie = request.POST.get('nombre_enfant_planifie') 
            nb_enfant_nplanifie = request.POST.get('nombre_enfant_non_planifie') 
            nb_fausse_couche = request.POST.get('fausse_couche') 
            nb_fausse_couche_intentionnelle = request.POST.get('fausse_couche_intentionnelle') 
            nb_enfant_hors_mariage = request.POST.get('enfant_hors_mariage') 

            if nb_fausse_couche == '' or nb_fausse_couche_intentionnelle == '':
                nb_fausse_couche= -1
                nb_fausse_couche_intentionnelle = -1

            grossesse = Grossesse.objects.create(
                id_personne=id_personne,
                planification=planification,
                meth_planification=meth_planification,
                envi_enfant=envi_enfant,
                nb_enfant=nb_enfant,
                nb_enfant_planifie=nb_enfant_planifie,
                nb_enfant_nplanifie=nb_enfant_nplanifie,
                nb_fausse_couche=nb_fausse_couche,
                nb_fausse_couche_intentionnelle=nb_fausse_couche_intentionnelle,
                nb_enfant_hors_mariage=nb_enfant_hors_mariage
            )
            

            #PrenatalMaternel oookkkkkkkk
            acc_serv_prenatal = request.POST.get('servicePrenatal')
            comp_grass = request.POST.get('complicationGrosse')
            desc_comp_gross = request.POST.get('motsClesComplicationsGrosses')
            comp_accouch = request.POST.get('complicationAccouchement')
            desc_comp_accouch = request.POST.get('motsClesComplicationsAccouchements')
            acc_serv_maternel = request.POST.get('serviceMaternel')
            meth_accouch = request.POST.get('methodeAccouchement')
            
            prenatal_maternel = PrenatalMaternel.objects.create(
                id_personne=id_personne,
                acc_serv_prenatal=acc_serv_prenatal,
                comp_grass=comp_grass,
                desc_comp_gross=desc_comp_gross,
                comp_accouch=comp_accouch,
                desc_comp_accouch=desc_comp_accouch,
                acc_serv_maternel=acc_serv_maternel,
                meth_accouch=meth_accouch
            )
        
            # Violence ooooooooooookkkkkkk
            taux_viol_sex = request.POST.get('violencesSexuelles') #Avez-vous déjà subi des violences sexuelles lors de rapports sexuels, combien ? *
            agress_sex = request.POST.get('agressionsSexuelles') #Avez-vous déjà été agressé sexuellement, combien de fois ? *
            taux_abus_viol_sex = request.POST.get('viols')
            soutien_psyc = request.POST.get('santeMentale') #Avez-vous eu recours à des services de santé mentale ? *
            type_harcelement_sex = request.POST.get('harcelementSexuel') #Avez-vous déjà été victime de harcèlement sexuel? (verbal, non-verbal, les deux) *
            taux_harcelement_sex = request.POST.get('nbr_harcel_sex') #Quel est le nombre d'harcélement sexuel ? *

            violence = Violence.objects.create(
                id_personne=id_personne,
                taux_viol_sex=taux_viol_sex,
                agress_sex= agress_sex,
                taux_abus_viol_sex=taux_abus_viol_sex,
                soutien_psyc=soutien_psyc,
                type_harcelement_sex=type_harcelement_sex,
                taux_harcelement_sex=taux_harcelement_sex
            )


            # Sr okkkkkkkkkk
            nb_verification_sr = request.POST.get('verificationSR') #int
            acc_service_examen = request.POST.get('serviceExamen') #char
            problemes_sex = request.POST.get('problemeSexuel') #char
            qualité_relation_sex = request.POST.get('satisfactionSexuelle') #char
            demande_soutien = request.POST.get('demandeSoutien') #char

            sr = Sr.objects.create(
                id_personne=id_personne,
                nb_verification_sr=nb_verification_sr,
                acc_service_examen=acc_service_examen,
                problemes_sex=problemes_sex,
                qualité_relation_sex=qualité_relation_sex,
                demande_soutien=demande_soutien
            )

            # Facteur okkk
            religion = request.POST.get('religion')
            niv_etud = request.POST.get('niveauEtudes')
            revenu = request.POST.get('revenu') #
            niv_social = request.POST.get('niveauSocial')
            impact_norme_culturelle = request.POST.get('normeCulturelle')
            impact_norme_religieuse = request.POST.get('normeReligieuse')

            facteur = Facteur.objects.create(
                id_personne=id_personne,
                religion=religion, 
                niv_etud=niv_etud, 
                revenu=revenu,
                niv_social=niv_social, 
                impact_norme_culturelle=impact_norme_culturelle,
                impact_norme_religieuse=impact_norme_religieuse
            )

            # Enquete oookkk
            doctorant = current_user_cin
            annee_realisation = datetime.now().year

            enquete = Enquete.objects.create(
                id_personne=id_personne,
                doctorant=doctorant, 
                annee_realisation=annee_realisation
            )

            return JsonResponse({'message': 'Formulaire soumis avec succès'})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Une erreur s\'est produite.'}, status=400)

def contacts(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')

    current_user_cin = request.session.get('user_cin')
    user_role = request.session.get('user_role')
    if user_role=='doctorant':
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nomComplet, role, email, telephone FROM doctorant WHERE cin != %s AND etat_compte = 'active' ",
                    [current_user_cin]
                )
                columns = [col[0] for col in cursor.description]
                data = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
        except DatabaseError as e:
            print(f"Database error: {e}")
            data = []

        return render(request, 'contacts.html', {'datas': data})
    redirect('login')




def personne(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    personnes = Personne.objects.all()  
    return render(request, 'personne.html', {'personnes': personnes})

def ist(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    ists = Ist.objects.all() 
    return render(request, 'ist.html', {'ists': ists})

def violence(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    violences = Violence.objects.all()  
    return render(request, 'violence.html', {'violences': violences})

def sr(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    srs = Sr.objects.all()  
    return render(request, 'sr.html', {'srs': srs})

def pratiques(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    pratiques = Pratique.objects.all()  
    return render(request, 'pratiques.html', {'pratiques': pratiques})

def grossesse(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    grossesses = Grossesse.objects.all()  
    return render(request, 'grossesse.html', {'grossesses': grossesses})

def facteur(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    facteurs = Facteur.objects.all()  
    return render(request, 'facteur.html', {'facteurs': facteurs})

def prenatal_maternel(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    prenatal_maternels = PrenatalMaternel.objects.all()  
    return render(request, 'prenatal_maternel.html', {'prenatal_maternels': prenatal_maternels})

def general (request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    else:
        generales = Generale.objects.all()  
        return render(request, 'general.html', {'generales': generales})




def projects(request):
    return render(request, 'projects.html')

def project_detail(request):
    return render(request, 'project_detail.html')


def profile(request):
    return render(request, 'profile.html')

def page_403(request):
    return render(request, 'page_403.html')

def page_404(request):
    return render(request, 'page_404.html')

def page_500(request):
    return render(request, 'page_500.html')

def plain_page(request):
    return render(request, 'plain_page.html')

def login_page(request):
    return render(request, 'login.html')

def pricing_tables(request):
    return render(request, 'pricing_tables.html')


def form_validation(request):
    return render(request, 'form_validation.html')

def form_wizard(request):
    return render(request, 'form_wizards.html')

def form_upload(request):
    return render(request, 'form_upload.html')

def form_buttons(request):
    return render(request, 'form_buttons.html')

def general_elements(request):
    return render(request, 'general_elements.html')

def media_gallery(request):
    return render(request, 'media_gallery.html')

def typography(request):
    return render(request, 'typography.html')

def icons(request):
    return render(request, 'icons.html')

def glyphicons(request):
    return render(request, 'glyphicons.html')

def widgets(request):
    return render(request, 'widgets.html')

def invoice(request):
    return render(request, 'invoice.html')

def inbox(request):
    return render(request, 'inbox.html')

def calendar(request):
    return render(request, 'calendar.html')

def tables(request):
    return render(request, 'tables.html')

def tables_dynamic(request):
    return render(request, 'tables_dynamic.html')

def chartjs(request):
    return render(request, 'chartjs.html')

def chartjs2(request):
    return render(request, 'chartjs2.html')

def morisjs(request):
    return render(request, 'morisjs.html')

def echarts(request):
    return render(request, 'echarts.html')

def other_charts(request):
    return render(request, 'other_charts.html')

def fixed_sidebar(request):
    return render(request, 'fixed_sidebar.html')

def fixed_footer(request):
    return render(request, 'fixed_footer.html')











def personne_edit(request, pk):
    personne = get_object_or_404(Personne, pk=pk)
    if request.method == "POST":
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            personne = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('personne')  
    else:
        form = PersonneForm(instance=personne)
    return render(request, 'personne_edit.html', {'form': form})
    

    
def pratiques_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    pratiques = get_object_or_404(Pratique, pk=pk)
    if request.method == "POST":
        form = PratiqueForm(request.POST, instance=pratiques)
        if form.is_valid():
            pratiques = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('pratiques')  
    else:
        form = PratiqueForm(instance=pratiques)
    return render(request, 'pratiques_edit.html', {'form': form})



def ist_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    ist = get_object_or_404(Ist, pk=pk)
    if request.method == "POST":
        form = IstForm(request.POST, instance=ist)
        if form.is_valid():
            ist=form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('ist')
    else:
        form = IstForm(instance=ist)
    return render(request, 'ist_edit.html', {'form': form})

def grossesse_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    grossesse = get_object_or_404(Grossesse, pk=pk)
    if request.method == "POST":   
        form = GrossesseForm(request.POST, instance=grossesse)
        if form.is_valid():
            grossesse = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('grossesse') 
    else:
        form = GrossesseForm(instance=grossesse)
    return render(request, 'grossesse_edit.html', {'form': form})

def facteur_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    facteur = get_object_or_404(Facteur, pk=pk)
    if request.method == "POST":
        form = FacteurForm(request.POST, instance=facteur)
        if form.is_valid():
            facteur = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('facteur')  
    else:
        form = FacteurForm(instance=facteur)
    return render(request, 'facteur_edit.html', {'form': form})




def prenatal_maternel_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    prenatal_maternel = get_object_or_404(PrenatalMaternel, pk=pk)
    if request.method == "POST":
        form = PrenatalMaternelForm(request.POST, instance=prenatal_maternel)
        if form.is_valid():
            prenatal_maternel = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('prenatal_maternel')  
    else:
        form = PrenatalMaternelForm(instance=prenatal_maternel)
    return render(request, 'prenatal_maternel_edit.html', {'form': form})

def violence_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    violence = get_object_or_404(Violence, pk=pk)
    if request.method == "POST":
        form = ViolenceForm(request.POST, instance=violence)
        if form.is_valid():
            violence = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('violence')  
    else:
        form = ViolenceForm(instance=violence)
    return render(request, 'violence_edit.html', {'form': form})

def sr_edit(request, pk):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    user_role = request.session.get('user_role')
    if user_role != 'doctorant':
        return redirect('login')
    sr= get_object_or_404(Sr, pk=pk)
    if request.method == "POST":
        form = SrForm(request.POST, instance=sr)
        if form.is_valid():
            sr = form.save()
            messages.success(request, "Enregistrement validé.")
            return redirect('sr') 
    else:
        form = SrForm(instance=sr)
    return render(request, 'sr_edit.html', {'form': form})


import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound
from .models import Personne

def archive(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')
    user_role = request.session.get('user_role')
    if user_role != 'responsable':
        return redirect('login')

    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))

    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            filename = fs.save(pdf_file.name, pdf_file)
            file_url = fs.url(filename)
        elif 'delete_file' in request.POST:
            filename = request.POST['delete_file']
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
            if os.path.exists(file_path):
                os.remove(file_path)

    # Liste des fichiers PDF dans le répertoire uploads
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    pdf_list = []
    for filename in os.listdir(uploads_dir):
        if filename.endswith('.pdf'):
            file_url = fs.url(os.path.join('uploads', filename))
            pdf_list.append({
                'title': filename,
                'description': 'Uploaded PDF file',
                'file_url': file_url,
                'filename': filename
            })

    return render(request, 'archive.html', {'pdf_list': pdf_list})
