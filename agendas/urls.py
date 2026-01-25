from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='agendas_index'),
    path('agendar-manutencao/', views.agendar_manutencao, name='agendar_manutencao'),
    path('report/<int:user_id>/', views.reportar_manutencao, name='reportar_manutencao'),
    path('report/processar/<int:agendamento_id>/', views.processar_finalizacao_agendamento, name='processar_finalizacao_agendamento'),
]
