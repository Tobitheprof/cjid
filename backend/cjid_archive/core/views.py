from django.shortcuts import render, redirect
from .tasks import *
from .models import *
from django.contrib import messages



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
    if request.method == "POST":
        title = request.POST['title']
        publication_date = request.POST['date']
        file = request.FILES.get('file')
        
        new_document = Document.objects.create(title=title, publication_date=publication_date, document=file)
        new_document.save()

        process_document_task.delay(new_document.pk)

        messages.success(f"Alright, the document processing has started. It might take sometime so just relax while the engine takes care of the work. The admin should an email once it's done processing")

        return redirect("process_document")

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
