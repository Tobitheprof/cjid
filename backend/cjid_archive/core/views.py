from django.shortcuts import render



def index(request):
    context = {
        'title' : 'Dashboard'
    }
    return render(request, 'index.html', context)

def archive(request):
    context = {
        'title' : 'Archive'
    }
    return render(request, 'archive.html', context)

def about(request):
    context = {
        'title' : 'About'
    }
    return render(request, 'about.html', context)

# Create your views here.
