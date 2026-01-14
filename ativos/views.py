from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Página de Ativos funcionando!")


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI, TipoUsuario.ALUNO, TipoUsuario.SERVIDOR])  
def equipamento(request):
    dados_do_equipamento = {
        "modelo": "Dell Optiplex 7090",
        "tipo": "Desktop Corporativo",
        "serial": "SNX-8745-DF92",
        "sala": "Salas A17",
        "fabricante": "Dell Technologies",
        "data_aquisicao": "15/07/2022",
        "data_garantia": "15/07/2025",
        "data_ultima_manutencao": "08/10/2024",
        "status": "defeituoso",
        "historico_manutencoes": [
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamentos com mau funcionamento na fonte",
                "responsavel": "Alexandre Magno",
                "data": "08/10/2024"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamentos com suspeita de vírus",
                "responsavel": "Maximus Decimos Meridios",
                "data": "25/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamentos com vírus em seu sistema operacional",
                "responsavel": "Carlos Magno",
                "data": "02/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Falha no cabo HDMI – substituição completa",
                "responsavel": "Tales de Mileto",
                "data": "02/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Revisão de rotina sem anomalias",
                "responsavel": "Carlos Drummond de Andrade",
                "data": "02/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamentos com suspeita de vírus",
                "responsavel": "Maximus Decimos Meridios",
                "data": "25/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamentos com vírus em seu sistema operacional",
                "responsavel": "Carlos Magno",
                "data": "02/10/2020"
            }
        ],
        "insights": [
            {
                "titulo": "Confiabilidade",
                "status": "ruim",
                "valor": "10%",
            },
            {
                "titulo": "Ultima verificação",
                "status": "ruim",
                "valor": "100 dias atrás",
            },
            {
                "titulo": "Tempo médio entre falhas",
                "status": "preocupante",
                "valor": "40 dias",
            },
            {
                "titulo": "Tendência de falhas",
                "status": "ruim",
                "valor": "Alta",
            },
            {
                "titulo": "Tempo médio de reparo",
                "status": "bom",
                "valor": "1h10",
            },
            {
                "titulo": "Recomendação de subistituição",
                "status": "preocupante",
                "valor": "50%",
            }
        ]
    }

    return render(request, 'ativos/paginas/base/pagina_de_equipamento/pagina_de_equipamento.html', dados_do_equipamento)
