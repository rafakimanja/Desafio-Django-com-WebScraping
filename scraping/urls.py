from django.urls import path
from scraping import views

urlpatterns = [
    path("", views.roda_script, name='script'),
]
