from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def index2(request):
    return render(request, 'index2.html')