from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        print("Hiiiiii")
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "Houda" and password == "Houda":
            return redirect('index')
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def index(request):
    return render(request, 'index.html')

def index2(request):
    return render(request, 'index2.html')

def index3(request):
    return render(request, 'index3.html')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
def e_commerce(request):
    # Logique de vue pour la page E-commerce
    return render(request, 'e_commerce.html')

def projects(request):
    # Logique de vue pour la page Projects
    return render(request, 'projects.html')

def project_detail(request):
    # Logique de vue pour la page Project Detail
    return render(request, 'project_detail.html')

def contacts(request):
    # Logique de vue pour la page Contacts
    return render(request, 'contacts.html')

def profile(request):
    # Logique de vue pour la page Profile
    return render(request, 'profile.html')

def page_403(request):
    # Logique de vue pour la page 403 Error
    return render(request, 'page_403.html')

def page_404(request):
    # Logique de vue pour la page 404 Error
    return render(request, 'page_404.html')

def page_500(request):
    # Logique de vue pour la page 500 Error
    return render(request, 'page_500.html')

def plain_page(request):
    # Logique de vue pour la page Plain Page
    return render(request, 'plain_page.html')

def login_page(request):
    # Logique de vue pour la page Login Page
    return render(request, 'login.html')

def pricing_tables(request):
    # Logique de vue pour la page Pricing Tables
    return render(request, 'pricing_tables.html')

from django.shortcuts import render

def form(request):
    return render(request, 'form.html')

def advanced_components(request):
    return render(request, 'advanced_components.html')

def form_validation(request):
    return render(request, 'form_validation.html')

def form_wizard(request):
    return render(request, 'form_wizard.html')

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
