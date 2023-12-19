from django.contrib import admin
from .models import Document, ExtractedImages

class ImageAdmin(admin.TabularInline):
    model = ExtractedImages

class DocumentAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ['title', 'publication_date', 'date_uploaded', 'document', 'short_extracted_text']

    def short_extracted_text(self, obj):
        # Adjust the character limit as per your requirement
        max_characters = 50
        if len(obj.extracted_text) > max_characters:
            return obj.extracted_text[:max_characters] + '...'
        else:
            return obj.extracted_text

    short_extracted_text.short_description = 'Extracted Text'

admin.site.register(Document, DocumentAdmin)
admin.site.register(ExtractedImages)
