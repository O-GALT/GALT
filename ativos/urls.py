from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ativos_index'),
    path('equipamento/', views.equipamento, name='equipamento'),
]
