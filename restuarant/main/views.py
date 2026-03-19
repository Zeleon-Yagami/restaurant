from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def aboutPage(request):
    return render(request, 'main/about.html')

def contactPage(request):
    return render(request, 'main/contact.html')

def menuPage(request):
    return render(request, 'main/menu.html')

def servicesPage(request):
    return render(request, 'main/services.html')