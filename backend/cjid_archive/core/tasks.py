# tasks.py

from celery import shared_task
from .models import Document, ExtractedImages
from .utils import save_pdf_as_images, extract_text_from_images
import os
from django.conf import settings

@shared_task
def process_document_task(document_id):
    try:
        document = Document.objects.get(pk=document_id)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, str(document.document))

        folder_name = save_pdf_as_images(uploaded_file_path)
        extracted_text = extract_text_from_images(folder_name)

        document.extracted_text = extracted_text
        document.save()

        image_files = os.listdir(folder_name)
        for image_file in image_files:
            image_path = os.path.join(folder_name, image_file)
            extracted_image = ExtractedImages(
                page_number=image_file,
                associated_document=document
            )
            extracted_image.image.save(image_file, open(image_path, 'rb'), save=True)
            print(f"Saved Image {image_file}")

    except Document.DoesNotExist:
        # Handle the case where the document does not exist
        pass
