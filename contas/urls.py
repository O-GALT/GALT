from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='contas_index'),
    path('@eu/', views.eu, name='contas_eu'),
    path('criar-recursos/', views.criar_recursos, name='criar_recursos'),
]
