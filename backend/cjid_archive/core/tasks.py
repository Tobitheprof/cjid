import os
from celery import shared_task
from django.conf import settings
from .models import Document, ExtractedImages
from .utils import save_pdf_as_images, extract_text_from_images

@shared_task
def process_document_task(document_id):
    try:
        document = Document.objects.get(pk=document_id)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, str(document.document))

        # Save images to the specified upload_to directory
        folder_name = save_pdf_as_images(uploaded_file_path)
        for image_file in os.listdir(folder_name):
            image_path = os.path.join(folder_name, image_file)
            image_instance = ExtractedImages(
                page_number=image_file,
                associated_document=document
            )
            # Save each image to the specified upload_to directory in the ExtractedImages model
            image_instance.image.save(image_file, open(image_path, 'rb'), save=True)
            print(f"Saved Image {image_file}")

        # Extract text from images
        extracted_text = extract_text_from_images(folder_name)
        document.extracted_text = extracted_text
        document.processing_status = 'COMPLETED'  # Update processing status
        document.save()

        # Clean up: Delete the text file
        os.remove(folder_name)  # Assuming 'folder_name' is the path to the text file

    except Document.DoesNotExist:
        # Handle the case where the document does not exist
        pass
