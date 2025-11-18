from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='contas_index'),
    path('@eu/', views.eu, name='contas_eu'),
    # URL QUE CRIEI APENAS PARA TESTAR A RENDERIZAÇÃO DO HEADER DE CRIACAO DE RECURSOS (se quiser, pode excluir)
    path('criar-recursos/', views.criar_recursos, name='criar_recursos'),
]
