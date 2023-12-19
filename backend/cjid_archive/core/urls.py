from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('archive', views.archive, name="archive"),
    path('about', views.about, name="about"),
    path('process-document', views.process_document, name="process_document"),
    path('document-detail/<str:pk>', views.document_detail, name="document_detail"),
]