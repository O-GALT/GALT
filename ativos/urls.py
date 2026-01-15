from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='ativos_index'),
    path('equipamentos/<int:equipamento_id>/', views.equipamento, name='ativos_equipamento_detail'),
]
