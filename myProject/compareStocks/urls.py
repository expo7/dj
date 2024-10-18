from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('definitions/', views.definitions, name='definitions'),
]

