from django.shortcuts import render, redirect, HttpResponseRedirect
import json, os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib import auth, messages
from django.db import connection
from .models import Personne

def login(request):
    # Nettoyer la session
    request.session.flush()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "houda" and password == "houda":
            request.session['user_authenticated'] = True    
            return HttpResponseRedirect(reverse('index'))
        elif username in ["afaf", "doha"] and password == username:  
            request.session['user_authenticated'] = True  
            return render(request, 'index2.html')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



def index(request):
    if not request.session.get('user_authenticated'):
        return redirect('login')  
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM PERSONNE")
            count = cursor.fetchone()[0]

    return render(request, 'index.html', {'count':count})

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
    if request.method == 'POST':
        print("Hello world")
        return render(request, 'enquetes.html')

    
    return render(request, 'enquetes.html', {'villes': villes, 'metiers': metiers})


def personne(request):
    return render(request, 'personne.html')

def ist(request):
    return render(request, 'ist.html')

def pratiques(request):
    return render(request, 'pratiques.html')

def grossesse(request):
    return render(request, 'grossesse.html')

def prenatal_maternel(request):
    return render(request, 'prenatal_maternel.html')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

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
