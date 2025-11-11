from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Página de Ativos funcionando!")


def equipamento(request):
    dados_do_equipamento = {
        "modelo": "Dell Optiplex 7090",
        "tipo": "Desktop Corporativo",
        "serial": "SNX-8745-DF92",
        "patrimonio": "PAT-00456",
        "fabricante": "Dell Technologies",
        "data_aquisicao": "15/07/2022",
        "data_garantia": "15/07/2025",
        "data_ultima_manutencao": "08/10/2024",
        "historico_manutencoes": [
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamento com mau funcionamento na fonte",
                "status": "Em andamento",
                "data": "08/10/2024"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamento com suspeita de vírus",
                "status": "Cancelada",
                "data": "25/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Equipamento com vírus em seu sistema operacional",
                "status": "Concluída",
                "data": "02/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Falha no cabo HDMI – substituição completa",
                "status": "Concluída",
                "data": "02/10/2020"
            },
            {
                "manutencao_id": "TASK-8782",
                "titulo": "Revisão de rotina sem anomalias",
                "status": "Concluída",
                "data": "02/10/2020"
            }
        ]
    }

    return render(request, 'ativos/pages/base/pagina_de_equipamento/pagina_de_equipamento.html', dados_do_equipamento)