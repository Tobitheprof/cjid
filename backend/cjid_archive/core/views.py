from django.shortcuts import render
from .tasks import *



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

def process_document(request):
    context = {
        'title' : "Process a Document"
    }
    return render(request, 'document_processing.html', context)

def document_detail(request):
    context = {
        'title' : "Detail"
    }
    return render(request, 'document_detail.html', context)
# Create your views here.
