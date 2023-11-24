from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_answer/",views.get_answer, name='get_answer'),
    path('process_question/', views.process_question, name='process_question'),
]