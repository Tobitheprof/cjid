from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('archive', views.archive, name="archive"),
    path('about', views.about, name="about")
]