from django.contrib import admin
from .models import *

class ImageAdmin(admin.TabularInline):
    model=ExtractedImages

class DocumentAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]
    list_display = ['title', 'publication_date', 'date_uploaded', 'document']

admin.site.register(Document, DocumentAdmin)
admin.site.register(ExtractedImages)

# Register your models here.