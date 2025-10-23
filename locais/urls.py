from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='locais_index'),
    path('salas/', views.salas, name='salas'),
    path('setores/', views.setores, name='setores'),
    path('predios/', views.predios, name='predios'),
]
