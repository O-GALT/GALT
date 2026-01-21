from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

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