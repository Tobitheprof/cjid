from django.shortcuts import render, redirect
from .tasks import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title' : 'Dashboard'
    }
    return render(request, 'index.html', context)

def archive(request):
    document_list = Document.objects.filter(processing_status="COMPLETE")
    
    # Number of documents to display per page
    per_page = 10  # Change this to your desired number of items per page
    
    paginator = Paginator(document_list, per_page)
    page_number = request.GET.get('page')
    
    try:
        documents = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        documents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        documents = paginator.page(paginator.num_pages)
    
    context = {
        'title': 'Archive',
        'documents': documents,
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
        
        new_document = Document.objects.create(title=title, publication_date=publication_date, document=file, processing_status="PENDING")
        new_document.save()

        from django.conf import settings
        media_url = settings.MEDIA_URL
        document_filename = new_document.document.name
        document_url = f"{media_url}documents/newspapers/{document_filename}"


        convert_pdf_to_images.delay(new_document.pk)
        print("STARTEDT TASK")

        # messages.info("Alright, the document processing has started. It might take sometime so just relax while the engine takes care of the work. The admin should an email once it's done processing")

        return redirect("process_document")

    context = {
        'title' : "Process a Document"
    }
    return render(request, 'document_processing.html', context)

def document_detail(request, pk):
    document = Document.objects.get(id=pk)
    context = {
        'title' : "Detail",
        'document' : document
    }
    return render(request, 'document_detail.html', context)
# Create your views here.
