from django.shortcuts import render, redirect
from .tasks import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

"""
For each bug and feature I either solve or create, I'll drop a dad joke.

1. What do you call a cow with no legs???
    Ground Beef(solved user auth bug)

2. Why are educated so hot???
    Cause they have more degress(Fixed mailing list bugs)

3. Why did the programmer need new glasses?
    Becaue he couldn't C# *ba dum tsss (Fixed Looping Issue With Maps API)

4. Why was 6 afraid of 7?
    Because 7, 8, 9(Fixed styling issue with maps)

5. What do you call a cow with no legs?
    Ground BEEF!!!!!!
"""

def index(request):
    context = {
        'title' : 'Dashboard'
    }
    return render(request, 'index.html', context)


def archive(request):
    document_list = Document.objects.filter(processing_status="COMPLETE")

    # Handling form submission
    keyword = request.GET.get('title')
    date_of_publication = request.GET.get('date')

    if keyword:
        document_list = document_list.filter(Q(title__icontains=keyword) | Q(extracted_text__icontains=keyword))

    if date_of_publication:
        document_list = document_list.filter(publication_date=date_of_publication)

    # Count the number of results
    num_results = document_list.count()

    # Pagination
    per_page = 10  # Change this to your desired number of items per page
    paginator = Paginator(document_list, per_page)
    page_number = request.GET.get('page')

    try:
        documents = paginator.page(page_number)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'title': 'Archive',
        'documents': documents,
        'num_results': num_results,
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

        messages.info(request, "Alright, the document processing has started. It might take sometime so just relax while the engine takes care of the work. The document should pop up in the archives once it's done processing")

        return redirect("process_document")

    context = {
        'title' : "Process a Document"
    }
    return render(request, 'document_processing.html', context)

def document_detail(request, pk):
    document = Document.objects.get(id=pk)
    context = {
        'title' : f"Detail | {document.title}",
        'document' : document
    }
    return render(request, 'document_detail.html', context)


def data_talk(request):
    context = {
        'title' : 'Talk with your data'
    }
    return render(request, 'data.html', context)
# Create your views here.
