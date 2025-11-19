from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kanban/', views.kanban, name='kanban_view'),
]
