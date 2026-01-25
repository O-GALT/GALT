from agendas.models import Agendamentos
from agendas.models import TecnicosTIAgendamentos

def formatar_agendamento(agendamento: Agendamentos):
    return {
        "id": agendamento.agendamento_id,
        "date": agendamento.data.strftime("%d/%m/%Y"),
        "hora_inicio": agendamento.inicio.strftime("%H:%M"),
        "hora_fim": agendamento.fim.strftime("%H:%M"),
        "descricao": agendamento.descricao,
        "estado": agendamento.estado_atual,
        "sala": {
            "id": agendamento.sala_id,
            "nome": "Sala " + agendamento.sala.localizacao,
        },
        "setor": {
            "id": agendamento.sala.setor.setor_id,
            "nome": agendamento.sala.setor.setor,
        },
        "predio": {
            "id": agendamento.sala.setor.predio.predio_id,
            "nome": agendamento.sala.setor.predio.predio,
        },
        "tecnicos_associados": listar_tecnicos(agendamento),
        "numero_tecnicos": len(listar_tecnicos(agendamento)),
    }


def listar_tecnicos(agendamento):
    tecnicos = TecnicosTIAgendamentos.objects.filter(agendamento=agendamento)
    tecnicos_list = []

    for tec in tecnicos:
        tecnicos_list.append({
            "nome" : tec.tecnico.usuario.nome,
            "email" : tec.tecnico.usuario.email
        })

    return tecnicos_list
