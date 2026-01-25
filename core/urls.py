from os import name

from django.urls import path, include
from django.contrib import admin
from core import views

urlpatterns = [
    path('', views.pagina_login, name='core_index_login'),

    path('login/', views.pagina_login, name='core_login'),
    path('criar-equipamento-modal', views.criar_equipamento_modal, name='criar_equipamento_modal'),
    path('criar-sala-modal', views.criar_sala_modal, name='criar_sala_modal'),
    path('concluido-modal', views.concluido_modal, name='concluido_modal'),
    path('criar-predio-modal', views.criar_predio_modal, name='criar_predio_modal'),
    path('criar-usuario-modal', views.criar_usuario_modal, name='criar_usuario_modal'),
    path('criar-setor-modal', views.criar_setor_modal, name='criar_setor_modal'),
    path('exclusao-modal', views.exclusao_modal, name='exclusao_modal'),

    path('equipamento-visao-usuario/<int:equipamento_id>/', views.equipamento_visao_usuario, name='equipamento_visao_usuario'),
    path('report-visao-usuario/<int:equipamento_id>/', views.report_visao_usuario, name='report_visao_usuario'),

    path('qr_code/<path:url>/', views.exibir_qr_code, name='gerar_qr_code'),

    path('qr-code/download/<path:url>/<str:identificador>', views.baixar_qr_code, name='baixar_qr_code')
]