from .models import Document
with open("C:\\Users\\user\\Documents\\cjid\\backend\\cjid_archive\\Resume_2_d_extracted_text.txt", 'r', encoding='utf-8') as text_file:
    extracted_text = text_file.read()

# print(extracted_text)


new_doc = Document.objects.get(id=30)

new_doc.extracted_text = extracted_text
new_doc.save()