from django.urls import path
from . import views
from .views import predios_equipamentos

urlpatterns = [
    path('', views.index, name='locais_index'),
    path('predios/<int:predio_id>/', views.predios, name='predio_detail'),
    path('predios/<int:predio_id>/setores/', views.predios_setores, name='predio_setores'),
    path('predios/<int:predio_id>/salas/', views.predios_salas, name='predio_salas'),
    path('predios/<int:predio_id>/equipamentos/', views.predios_equipamentos, name='predio_equipamentos'),
    path('setores/<int:setor_id>/', views.setores, name='setor_detail'),
    path('salas/<int:sala_id>/', views.salas, name='sala_detail'),

    # URL'S QUE USEI DE TESTE PARA TESTAR RENDERIZAÇÃO DA SELECAO DE EQUIPAMENTOS E SALAS NA PARTE DO PREDIO PRINCIPAL(se quiser, pode excluir)
    # path('predios/equipamentos/', views.predios_equipamentos, name='predios_equipamentos'),
    # path('predios/salas/', views.predios_salas, name='predios_salas'),
]
