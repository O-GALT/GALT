from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='locais_index'),
    path('salas/', views.salas, name='salas'),
    path('setores/', views.setores, name='setores'),
    path('predios/', views.predios, name='predios'),

    # URL'S QUE USEI DE TESTE PARA TESTAR RENDERIZAÇÃO DA SELECAO DE EQUIPAMENTOS E SALAS NA PARTE DO PREDIO PRINCIPAL(se quiser, pode excluir)
    # path('predios/equipamentos/', views.predios_equipamentos, name='predios_equipamentos'),
    # path('predios/salas/', views.predios_salas, name='predios_salas'),
]
