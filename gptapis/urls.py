from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('process_question/', views.process_question, name='process_question'),
]