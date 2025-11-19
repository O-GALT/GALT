from datetime import date

from django.shortcuts import render
from django.http import HttpResponse

from auditoria.models import AuditoriaLog
from contas.models import Usuario
from core.essenciais import TipoUsuario, Acao, TipoAlvo


# Create your views here.
def index(request):
    context = {}
    context['tipo_autores'] = [TipoUsuario.PROFESSOR.label, TipoUsuario.ALUNO.label, TipoUsuario.TECNICO_TI.label, TipoUsuario.ADMINISTRADOR.label, TipoUsuario.ROOT.label]
    context['autores'] = ['@lucas Rian', '@Marcos Silva', '@Vanessa Cortez', '@Kayke Alves', '@Mariana Paiva', '@Yara Paiva']
    context['acoes'] = [Acao.CRIAR_USUARIO.label, Acao.DELETAR_USUARIO.label, Acao.ATUALIZAR_USUARIO.label, Acao.CRIAR_SALA.label, Acao.DELETAR_SALA.label, Acao.ATUALIZAR_SALA.label, Acao.CRIAR_PREDIO.label, Acao.ATUALIZAR_PREDIO.label, Acao.DELETAR_PREDIO.label, Acao.CRIAR_SETOR.label, Acao.ATUALIZAR_SETOR.label, Acao.DELETAR_SETOR.label, Acao.CRIAR_AGENDAMENTO.label, Acao.ATUALIZAR_AGENDAMENTO.label, Acao.DELETAR_AGENDAMENTO.label, Acao.ABRIR_REPORTE.label, Acao.TROCAR_EQUIPAMENTO_SALA.label]
    context['alvo_acao'] = [TipoAlvo.ALUNO.label, TipoAlvo.ROOT.label, TipoAlvo.PROFESSOR.label, TipoAlvo.ADMINISTRADOR.label, TipoAlvo.AGENDAMENTO.label, TipoAlvo.AR_CONDICIONADO.label, TipoAlvo.COMPUTADOR.label, TipoAlvo.PREDIO.label, TipoAlvo.PROJETOR.label, TipoAlvo.SALA.label, TipoAlvo.SETOR.label]
    context['auditorias'] = [AuditoriaLog(auditoria_id=1, user=Usuario(email_escolar='Thaua@escolar.com', tipo_usuario=TipoUsuario.ALUNO.label), acao=Acao.ABRIR_REPORTE.label, tipo_alvo=TipoAlvo.REPORTE.label, data=date.today()), AuditoriaLog(auditoria_id=2, user=Usuario(email_escolar='Vanessa@escolar.com', tipo_usuario=TipoUsuario.TECNICO_TI.label), acao=Acao.CRIAR_AGENDAMENTO.label, tipo_alvo=TipoAlvo.AGENDAMENTO.label, data=date.today()), AuditoriaLog(auditoria_id=3, user=Usuario(email_escolar='Kayke@escolar.com', tipo_usuario=TipoUsuario.TECNICO_TI.label), acao=Acao.TROCAR_EQUIPAMENTO_SALA.label, tipo_alvo=TipoAlvo.PROJETOR.label, data=date.today()), AuditoriaLog(auditoria_id=4, user=Usuario(email_escolar='Yara@escolar.com', tipo_usuario=TipoUsuario.ADMINISTRADOR.label), acao=Acao.CRIAR_SETOR.label, tipo_alvo=TipoAlvo.SETOR.label, data=date.today()), AuditoriaLog(auditoria_id=5, user=Usuario(email_escolar='Mariana@escolar.com', tipo_usuario=TipoUsuario.ROOT.label), acao=Acao.CRIAR_USUARIO.label, tipo_alvo=TipoAlvo.ALUNO.label, data=date.today()), AuditoriaLog(auditoria_id=6, user=Usuario(email_escolar='Salatiel@escolar.com', tipo_usuario=TipoUsuario.ALUNO.label), acao=Acao.ABRIR_REPORTE.label, tipo_alvo=TipoAlvo.REPORTE.label, data=date.today()),AuditoriaLog(auditoria_id=7, user=Usuario(email_escolar='Vitoria@escolar.com', tipo_usuario=TipoUsuario.ADMINISTRADOR.label), acao=Acao.DELETAR_AGENDAMENTO.label, tipo_alvo=TipoAlvo.AGENDAMENTO.label, data=date.today())]
    context['objetos'] = [
        {'auditoria_id': '1', 'tipo_autor': 'Thunder V12', 'autor': 'Thauã@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reporte', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': 'Thunder V12', 'autor': 'Thauã@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reporte', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': 'Thunder V12', 'autor': 'Thauã@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reporte', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': 'Thunder V12', 'autor': 'Thauã@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reporte', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': 'Thunder V12', 'autor': 'Thauã@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reporte', 'data': date.today()},
    ]
    return HttpResponse(render(request, 'auditoria/paginas/auditoria.html', context))

# VIEW QUE CRIEI PARA TESTAR A RENDERIZACAO DO HEADER DA PAGINA DE AUDITORIA(se quiser, pode excluir)
# def index(request):
#     return HttpResponse(render(request, 'auditoria/partials/headers/auditoria_header.html'))
