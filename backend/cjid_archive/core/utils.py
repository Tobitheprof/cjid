import fitz
import os
import pytesseract

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

def extract_text_from_images(folder_name):
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
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(extracted_text)

    print(f"All extracted text has been saved to {output_text_file}")

