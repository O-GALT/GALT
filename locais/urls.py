from codecs import namereplace_errors

from django.urls import path
from . import views
from .views import predios_equipamentos
urlpatterns = [
    path('predios/', views.home, name='home'),
    path('predios/<int:predio_id>/', views.predios, name='locais_predio_detail'),
    path('predios/<int:predio_id>/setores/', views.predios_setores, name='locais_predio_setores'),
    path('predios/<int:predio_id>/salas/', views.predios_salas, name='locais_predio_salas'),
    path('predios/<int:predio_id>/equipamentos/', views.predios_equipamentos, name='locais_predio_equipamentos'),
    path('setores/<int:setor_id>/', views.setores, name='locais_setor_detail'),
    path('salas/<int:sala_id>/', views.salas, name='locais_sala_detail'),

    path('salas/tocar-equipamento/', views.trocar_equipamento_sala, name='locais_trocar_equipamento_sala'),

    path('predio/grafico-estado-equipamentos/<int:predio_id>/', views.renderizar_grafico_estado_equipamentos_predio, name='locais_renderizar_estado_equipamentos_predio'),
    path('predio/grafico-saude-predio/<int:predio_id>/', views.renderizar_grafico_saude_predio, name='locais_renderizar_saude_predio'),
    path('predio/grafico-estado-salas/<int:predio_id>/', views.renderizar_grafico_estado_salas_predio, name='locais_renderizar_estado_salas_predio'),
    path('predio/reportes-tipo-equipamento/<int:predio_id>/', views.renderizar_reporte_por_tipo_equipamento_predio, name='locais_renderizar_reportes_tipo_equipamento_predio'),
    path('predio/indice-manutencoes/<int:predio_id>/', views.renderizar_grafico_indice_manutencao, name='renderizar_grafico_indice_manutencoes_predio'),


    path('setor/grafico-estado-salas/<int:setor_id>/', views.renderizar_grafico_estado_salas_setor, name='locais_renderizar_estado_salas_setor'),
    path('setor/grafico-estado-equipamentos/<int:setor_id>/', views.renderizar_grafico_estado_equipamentos_setor, name='locais_renderizar_estado_equipamentos_setor'),
    path('setor/grafico-saude-setor/<int:setor_id>/', views.renderizar_grafico_saude_setor, name='locais_renderizar_saude_setor'),
    path('setor/reportes-tipo-equipamento/<int:setor_id>/', views.renderizar_grafico_reporte_por_tipo_setor, name='locais_renderizar_reportes_tipo_equipamento_setor'),

    # URL'S QUE USEI DE TESTE PARA TESTAR RENDERIZAÇÃO DA SELECAO DE EQUIPAMENTOS E SALAS NA PARTE DO PREDIO PRINCIPAL(se quiser, pode excluir)
    # path('predios/equipamentos/', views.predios_equipamentos, name='predios_equipamentos'),
    # path('predios/salas/', views.predios_salas, name='predios_salas'),
]

