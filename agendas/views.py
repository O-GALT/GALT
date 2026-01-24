from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from agendas.models import TecnicosTIAgendamentos, Agendamentos
from contas.models import TecnicosTI
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario
from core.schedule.jobs import Jobs
from locais.models import Salas
import json


# Create your views here.

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def index(request):
    context = {}

    context['pendentes'] = {
        "cards": [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
                "descricao": "Manutenção preventiva dos equipamentos da sala A17."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala B12",
                "nome_setor": "Setor acadêmico",
                "nome_predio": "Bloco B",
                "hora_inicio": "10:40",
                "hora_fim": "12:00",
                "numero_tecnicos": 3,
                "descricao": "Ajuste de projetor e verificação de cabeamento."
            },
        ],
        "count": 2
    }

    context['em_andamento'] = {
        "cards": [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala C03",
                "nome_setor": "Laboratórios",
                "nome_predio": "Prédio técnico",
                "hora_inicio": "08:00",
                "hora_fim": "09:30",
                "numero_tecnicos": 4,
                "descricao": "Atualização de software nos computadores do laboratório."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "09:10",
                "hora_fim": "10:30",
                "numero_tecnicos": 5,
                "descricao": "Correção de falhas elétricas identificadas anteriormente."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Auditório",
                "nome_setor": "Eventos",
                "nome_predio": "Bloco Central",
                "hora_inicio": "13:00",
                "hora_fim": "15:00",
                "numero_tecnicos": 6,
                "descricao": "Preparação de áudio e vídeo para evento institucional."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala D08",
                "nome_setor": "Setor administrativo",
                "nome_predio": "Bloco D",
                "hora_inicio": "15:30",
                "hora_fim": "17:00",
                "numero_tecnicos": 2,
                "descricao": "Troca de equipamentos danificados."
            },
        ],
        "count": 4
    }

    context['feedback'] = {
        "cards": [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala E01",
                "nome_setor": "Setor pedagógico",
                "nome_predio": "Anexo",
                "hora_inicio": "09:00",
                "hora_fim": "10:00",
                "numero_tecnicos": 1,
                "descricao": "Aguardando validação do solicitante após manutenção."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala F10",
                "nome_setor": "Biblioteca",
                "nome_predio": "Bloco F",
                "hora_inicio": "11:00",
                "hora_fim": "12:30",
                "numero_tecnicos": 2,
                "descricao": "Feedback pendente sobre funcionamento dos computadores."
            },
        ],
        "count": 2
    }

    context['inacabado'] = {
        "cards": [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala G05",
                "nome_setor": "Setor técnico",
                "nome_predio": "Bloco G",
                "hora_inicio": "14:00",
                "hora_fim": "16:00",
                "numero_tecnicos": 3,
                "descricao": "Serviço interrompido por falta de material."
            },
        ],
        "count": 1
    }

    context['finalizado'] = {
        "cards": [
            {
                "date": "25/01/2026",
                "nome_sala": "Sala H02",
                "nome_setor": "Setor de informática",
                "nome_predio": "Bloco H",
                "hora_inicio": "08:30",
                "hora_fim": "09:30",
                "numero_tecnicos": 2,
                "descricao": "Instalação concluída com sucesso."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala A17",
                "nome_setor": "Setor de salas de aulas",
                "nome_predio": "Prédio principal",
                "hora_inicio": "10:00",
                "hora_fim": "11:00",
                "numero_tecnicos": 3,
                "descricao": "Reparo finalizado e validado."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala J09",
                "nome_setor": "Pesquisa",
                "nome_predio": "Bloco J",
                "hora_inicio": "13:30",
                "hora_fim": "14:30",
                "numero_tecnicos": 1,
                "descricao": "Configuração de rede concluída."
            },
            {
                "date": "25/01/2026",
                "nome_sala": "Sala K11",
                "nome_setor": "Coordenação",
                "nome_predio": "Bloco K",
                "hora_inicio": "16:00",
                "hora_fim": "17:30",
                "numero_tecnicos": 4,
                "descricao": "Manutenção corretiva finalizada."
            },
        ],
        "count": 4
    }

    return render(request, 'agendas/pages/kanban/kanban.html', context)


def agendar_manutencao(request):
    next = request.POST['next_url']
    sala_id = request.POST['sala']
    tecnicos_id = request.POST['tecnicos']
    data_manutencao = request.POST['data_manutencao']
    horario_inicio = request.POST['horario_inicio']
    horario_final = request.POST['horario_final']
    descricao = request.POST['descricao']

    if not sala_id or not tecnicos_id or not data_manutencao or not horario_inicio or not horario_final or not descricao:
        return HttpResponseRedirect(next)

    tecnicos_id = list(map(int, json.loads(tecnicos_id)))

    tecnicos = TecnicosTI.objects.filter(usuario_id__in=tecnicos_id)
    sala = Salas.carregar(sala_id)


    agendamento = Agendamentos(
        sala=sala,
        inicio=horario_inicio,
        fim=horario_final,
        data=data_manutencao,
    )

    agendamento.save()

    for tecnico in tecnicos:
        tecnico_agendamento = TecnicosTIAgendamentos(
            tecnico=tecnico,
            agendamento=agendamento,
            responsavel= True if request.user.id == tecnico.usuario.id else False
        )
        tecnico_agendamento.save()

    Jobs.setar_comportamento_agendamento_inicio_e_fim(agendamento)
    return HttpResponseRedirect(next)