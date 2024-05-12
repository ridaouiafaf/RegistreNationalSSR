from django.shortcuts import render, redirect
import json, os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib import auth, messages
from django.db import connection
from .models import Personne
from django.views.decorators.cache import never_cache
from .models import *
from django.db.models import Max
from django.http import JsonResponse

@never_cache
def login(request):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "Houda" and password == "Houda":
            request.session['user_authenticated'] = True  
            return redirect('index')
        elif username == "afaf" and password == "afaf":
            request.session['user_authenticated'] = True  
            return redirect('index2')
        elif username == "doha" and password == "doha":
            request.session['user_authenticated'] = True  
            return redirect('index2')
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def index(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM PERSONNE")
            count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'H'")
            count_h = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM PERSONNE WHERE SEXE like 'F'")
            count_f = cursor.fetchone()[0]


    return render(request, 'index.html', {'personne':count, 'homme':count_h, 'femme':count_f})

def index2(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    return render(request, 'index2.html')

def index3(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    return render(request, 'index3.html')

def enquetes(request):
    current_directory = os.path.dirname(__file__)+'\\templates'
    metiers = os.path.join(current_directory, 'métiers.json')
    villes = os.path.join(current_directory, 'villes.json')
    with open(villes, 'r', encoding='utf-8') as file:
        villes = json.load(file)
    with open(metiers, 'r', encoding='utf-8') as file:
        metiers = json.load(file)
    return render(request, 'enquetes.html', {'villes': villes, 'metiers': metiers})



def enquete_soumis(request):
    if request.method == 'POST' :
 
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
        print(id_personne)

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
        envi_enfant = request.POST.get('envi_enfant') 
        nb_enfant = request.POST.get('nombre_enfant') 
        nb_enfant_planifie = request.POST.get('nombre_enfant_planifie') 
        nb_enfant_nplanifie = request.POST.get('nombre_enfant_non_planifie') 
        nb_fausse_couche = request.POST.get('fausse_couche') 
        nb_fausse_couche_intentionnelle = request.POST.get('fausse_couche_intentionnelle') 
        nb_enfant_hors_mariage = request.POST.get('enfant_hors_mariage') 

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
        doctorant = request.POST.get('doctorant')
        annee_realisation = request.POST.get('anneeRealisation')

        enquete = Enquete.objects.create(
            id_personne=id_personne,
            doctorant=doctorant, 
            annee_realisation=annee_realisation
        )

        return JsonResponse({'message': 'Formulaire '})
    return JsonResponse({'message': 'Une erreur s\'est produite.'}, status=400)


def personne(request):
    return render(request, 'personne.html')

def violence(request):
    return render(request, 'violence.html')

def sr(request):
    return render(request, 'sr.html')

def ist(request):
    return render(request, 'ist.html')

def general(request):
    return render(request, 'general.html')

def pratiques(request):
    return render(request, 'pratiques.html')

def grossesse(request):
    return render(request, 'grossesse.html')
def facteur(request):
    return render(request, 'facteur.html')

def prenatal_maternel(request):
    return render(request, 'prenatal_maternel.html')


def projects(request):
    return render(request, 'projects.html')

def project_detail(request):
    return render(request, 'project_detail.html')

def contacts(request):
    return render(request, 'contacts.html')

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

def form(request):
    return render(request, 'form.html')

def advanced_components(request):
    return render(request, 'advanced_components.html')

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



