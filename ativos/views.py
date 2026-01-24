from django.contrib.auth.decorators import login_required

from ativos.models import HistoricoManutencoes, Equipamentos
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario, TipoEquipamento, EstadoEquipamento, Fileira

from django.shortcuts import render
from django.http import HttpResponse

from core.sql.SQLNativo import SQLNativo
from locais.models import Salas
from suporte.models import Reportes


# Create your views here.

def index(request):
    return HttpResponse("Página de Ativos funcionando!")


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def equipamento(request, equipamento_id):
    info_equipamento = SQLNativo.carregar_indicadores_equipamento(equipamento_id)[0]
    dados_do_equipamento = {
        'qr_code_url': 'equipamento_visao_usuario,' + str(equipamento_id),
        "modelo": "Dell Optiplex 7090",
        "tipo": TipoEquipamento(info_equipamento['tipo']).label,
        'classe_estado': info_equipamento['estado_atual'],
        'estado_atual': EstadoEquipamento(info_equipamento['estado_atual']).label,
        'reportes_abertos': info_equipamento['reportes_abertos'],
        'manutencoes_realizadas': info_equipamento['manutencoes_realizadas'],
        "serial": info_equipamento['serial'],
        "sala": "Sala " + info_equipamento['sala'],
        "fabricante": info_equipamento['fabricante'],
        "data_aquisicao": info_equipamento['data_aquisicao'],
        "data_ultima_manutencao": info_equipamento['data_ultima_manutencao'],
        "status": info_equipamento['estado_atual'],
        'salas': Salas.listar_salas(),
        'equipamentos': Equipamentos.listar_equipamentos(),
        'fileiras_sala': list(Fileira),
        'info_reportes_abertos': [reporte for reporte in Reportes.listar_reportes_equipamento(equipamento_id)],
        'historico_manutencoes': [{"manutencao_id": historico['historico_manutencoes_id'], "titulo":historico['titulo'], "responsavel":historico['responsavel'], "data":historico['data']} for historico in HistoricoManutencoes.listar_historico_equipamento(equipamento_id)],
        'next': request.path,
        "insights": [
            {
                "titulo": "Última manuteção",
                "status": "boa",
                "valor": str(info_equipamento['ultima_manutencao']) + " dias atrás",
            },
            {
                "titulo": "Manutenções preventivas",
                "status": "preocupante",
                "valor": info_equipamento['manutencoes_preventivas'],
            },
            {
                "titulo": "Tempo médio entre falhas",
                "status": "preocupante",
                "valor": str(info_equipamento['tempo_medio_entre_falhas']) + " dias",
            },
            {
                "titulo": "Tendência de falhas",
                "status": "ruim",
                "valor": info_equipamento['tedencias_a_falhas'],
            },
            {
                "titulo": "Manutenções nesse mês",
                "status": "preocupante",
                "valor": info_equipamento['manutencoes_nesse_mes'],
            },
            {
                "titulo": "Recomendação de subistituição",
                "status": "ruim",
                "valor": str(info_equipamento['recomendacao_substituicao']) + "%",
            }
        ]
    }

    return render(request, 'ativos/paginas/base/pagina_de_equipamento/pagina_de_equipamento.html', dados_do_equipamento)
