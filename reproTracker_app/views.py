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