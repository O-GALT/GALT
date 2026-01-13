from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    context['pendentes'] = {
        "cards" : [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
            },
        ],
        "count" : 2
    }

    context['em_andamento'] = {
        "cards" : [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
            },
        ],
        "count" : 2
    }

    context['feedback'] = {
        "cards" : [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
            },
        ],
        "count" : 2
    }

    context['inacabado'] = {
        "cards" : [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
            },
        ],
        "count" : 2
    }

    context['finalizado'] = {
        "cards" : [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
            },
        ],
        "count" : 2
    }


    return render(request, 'agendas/pages/kanban/kanban.html' , context)