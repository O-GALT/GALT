from ativos.models import Equipamentos
from locais.models import Salas


def formatar_lista_de_equipamentos_concertados(sala_id):
    equipamentos = Equipamentos.listar_por_sala(sala_id)
    sala_atual = Salas.carregar(sala_id)

    equipamentos_formatados = []

    for equipamento in equipamentos:
        equipamentos_formatados.append({
            "equipamento_id": equipamento.equipamento_id,
            "sala_id": equipamento.sala_id,
            "sala" : "Sala " + sala_atual.localizacao,
            "posicao": "Posição " + str(equipamento.posicao),
            "tipo": equipamento.tipo,
            "serial": equipamento.serial,
            "estado_atual": equipamento.estado_atual,
            "fabricante": equipamento.fabricante,
            "data_aquisicao": equipamento.data_aquisicao,
        })

    return equipamentos_formatados
