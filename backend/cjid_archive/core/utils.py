import fitz
import os
import pytesseract
from .models import *
def save_pdf_as_images(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Get the title of the PDF (assuming the title is the name of the file without the extension)
    title = os.path.splitext(os.path.basename(pdf_path))[0]

    # Create a folder with the title and a unique identifier
    folder_name = f"{title}_d"
    os.makedirs(folder_name, exist_ok=True)

    # Iterate through each page of the PDF
    for i in range(doc.page_count):
        page = doc[i]
        pix = page.get_pixmap(dpi=400)
        
        # Save the image with a unique name inside the created folder
        image_name = f"page_{i + 1}.jpg"
        image_path = os.path.join(folder_name, image_name)
        pix.save(image_path)
    
    # Close the PDF document
    doc.close()

    return folder_name

def extract_text_from_images(folder_name, document_id):
    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(folder_name) if f.endswith('.jpg')]

    extracted_text = ''

    # Loop through each image file and extract text using Tesseract OCR
    for image_file in image_files:
        image_path = os.path.join(folder_name, image_file)
        
        # Perform OCR using pytesseract
        extracted_text += pytesseract.image_to_string(image_path)

    # Save all extracted text into a single text file
    output_text_file = f"{folder_name}_extracted_text.txt"
    with open(output_text_file, 'rb', encoding='utf-8') as text_file:
        text_read = text_file.read(extracted_text)
    new_doc_instance = Document.objects.get(id=document_id)
    new_doc_instance.extracted_text = text_read
    new_doc_instance.save()
    print(extracted_text)

    print(f"All extracted text has been saved to {output_text_file}")

    # Read the content of the text file and return the extracted text
    with open(output_text_file, 'r', encoding='utf-8') as text_file:
        extracted_text_from_file = text_file.read()

    # new_doc_instance = Document.objects.get(id=document_id)
    # new_doc_instance.extracted_text = extracted_text_from_file
    # new_doc_instance.save()

    return extracted_text_from_file