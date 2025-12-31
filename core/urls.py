from django.urls import path, include
from django.contrib import admin
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login', views.login, name='login'),

    path('criar-equipamento-modal', views.criar_equipamento_modal, name='criar_equipamento_modal'),
    path('criar-sala-modal', views.criar_sala_modal, name='criar_sala_modal'),
    path('concluido-modal', views.concluido_modal, name='concluido_modal'),
    path('criar-predio-modal', views.criar_predio_modal, name='criar_predio_modal'),
    path('criar-usuario-modal', views.criar_usuario_modal, name='criar_usuario_modal'),
    path('criar-setor-modal', views.criar_setor_modal, name='criar_setor_modal'),
    path('exclusao-modal', views.exclusao_modal, name='exclusao_modal'),

    path('equipamento-visao-usuario', views.equipamento_visao_usuario, name='equipamento_visao_usuario'),
    path('report-visao-usuario', views.report_visao_usuario, name='report_visao_usuario'),
]