from celery import shared_task
from .models import Document, ExtractedImages
from .utils import save_pdf_as_images, extract_text_from_images
import os
from django.conf import settings

@shared_task
def extract_images_task(document_id):
    try:
        document = Document.objects.get(pk=document_id)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, str(document.document))

        folder_name = save_pdf_as_images(uploaded_file_path)
        print(f"Images saved in folder: {folder_name}")

        # Rest of your code to save extracted images...
        image_files = os.listdir(folder_name)
        for image_file in image_files:
            image_path = os.path.join(folder_name, image_file)
            try:
                extracted_image = ExtractedImages(
                    page_number=image_file,
                    associated_document=document
                )
                extracted_image.image.save(image_file, open(image_path, 'rb'), save=True)
                print(f"Saved Image {image_file}")
            except Exception as e:
                print(f"Error saving image {image_file}: {e}")

        # Trigger the text extraction task once image extraction is completed
        extract_text_task.delay(document_id, folder_name)  # Call the text extraction task

    except Document.DoesNotExist:
        print(f"Document with ID {document_id} does not exist.")
    except Exception as e:
        print(f"Error extracting images: {e}")




@shared_task
def extract_text_task(document_id, folder_name):
    try:
        document = Document.objects.get(pk=document_id)

        # Extract text from images
        extraction_result = extract_text_from_images(folder_name)

        if extraction_result and len(extraction_result) == 2:
            extracted_text, text_file_path = extraction_result

            if extracted_text is not None and text_file_path is not None:
                with open(text_file_path, 'r', encoding='utf-8') as text_file:
                    extracted_text = text_file.read()

                document.extracted_text = extracted_text
                document.title = "Shit Head"
                document.save()
                print("Document updated successfully with extracted text!")
            else:
                print("No text extracted or text extraction failed.")
        else:
            print("Error: Text extraction did not return expected values.")

    except Document.DoesNotExist:
        print(f"Document with ID {document_id} does not exist.")
    except Exception as e:
        print(f"Error extracting text: {e}")
