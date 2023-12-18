from django.db import models
import uuid

PROCESS_STATUS = (
    ('IN PROGRESS', 'IN PROGRESS'),
    ('PENDING', 'PENDING'),
    ('COMPLETE', 'COMPLETE'),
)


class Document(models.Model):
    title = models.CharField(max_length=200, unique=True)
    publication_date = models.DateField()
    date_uploaded = models.DateField(auto_now_add=True)
    extracted_text = models.TextField(null=True)
    document = models.FileField(upload_to="documents/newspapers")
    processing_status = models.CharField(max_length=200, choices=PROCESS_STATUS)


    def __str__(self):
        return f"{self.title}"
    
class ExtractedImages(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    page_number = models.CharField(max_length=300)
    associated_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="newspapers/extracted_images")

    def __str__(self):
        return f"{self.id}-{self.page_number}"

# Create your models here.