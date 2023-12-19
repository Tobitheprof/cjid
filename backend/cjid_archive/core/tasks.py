from celery import shared_task
import fitz  # PyMuPDF
from .models import Document, ExtractedImages
from celery import shared_task
import pytesseract
import os
from .utils import *
from io import BytesIO
from PIL import Image as PILImage

@shared_task
def convert_pdf_to_images(document_id, target_dpi=300):
    try:
        document = Document.objects.get(id=str(document_id))
        pdf_document = document.document.path

        pdf = fitz.open(pdf_document)
        
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            
            # Calculate image size based on DPI
            zoom_x = target_dpi / 72.0
            zoom_y = target_dpi / 72.0
            mat = fitz.Matrix(zoom_x, zoom_y)
            pixmap = page.get_pixmap(matrix=mat)
            
            pil_image = PILImage.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            
            # Save PIL image to a buffer
            image_buffer = BytesIO()
            pil_image.save(image_buffer, format='PNG')
            image_buffer.seek(0)
            
            image_path = f"newspapers/extracted_images/{document_id}_page_{page_num + 1}.png"
            image_file = ExtractedImages()
            image_file.page_number = str(page_num + 1)
            image_file.associated_document = document
            image_file.image.save(image_path, image_buffer)
            
        pdf.close()
        
        extract_text_from_images.delay(document_id)

        document.processing_status = 'IN PROGRESS'
        document.save()

    except Document.DoesNotExist:
        pass  # Handle exception appropriately


@shared_task
def extract_text_from_images(document_id):
    try:
        document = Document.objects.get(id=str(document_id))
        
        # Gather all images associated with the document
        images = ExtractedImages.objects.filter(associated_document=document)
        
        # Extract text from each image using PyTesseract
        extracted_text = ''
        for image in images:
            img_text = pytesseract.image_to_string(image.image.path)
            extracted_text += img_text + '\n\n'
        
        # Save the extracted text to the Document model
        document.extracted_text = extracted_text
        document.processing_status = 'COMPLETE'
        document.save()

    except Document.DoesNotExist:
        pass  # Handle exception appropriately