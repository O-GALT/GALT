from datetime import date

from django.shortcuts import render
from django.http import HttpResponse

from auditoria.models import AuditoriaLog
from contas.models import Usuarios
from core.essenciais import TipoUsuario, Acao, TipoAlvo


# Create your views here.
def index(request):
    context = {}
    context['tipo_autores'] = [TipoUsuario.SERVIDOR.label, TipoUsuario.ALUNO.label, TipoUsuario.TECNICO_TI.label,
                               TipoUsuario.ADMINISTRADOR.label]
    context['autores'] = ['@lucas Rian', '@Marcos Silva', '@Vanessa Cortez', '@Kayke Alves', '@Mariana Paiva',
                          '@Yara Paiva']
    context['acoes'] = [Acao.CRIAR_USUARIO.label, Acao.DELETAR_USUARIO.label, Acao.ATUALIZAR_USUARIO.label,
                        Acao.CRIAR_SALA.label, Acao.DELETAR_SALA.label, Acao.ATUALIZAR_SALA.label,
                        Acao.CRIAR_PREDIO.label, Acao.ATUALIZAR_PREDIO.label, Acao.DELETAR_PREDIO.label,
                        Acao.CRIAR_SETOR.label, Acao.ATUALIZAR_SETOR.label, Acao.DELETAR_SETOR.label,
                        Acao.CRIAR_AGENDAMENTO.label, Acao.ATUALIZAR_AGENDAMENTO.label, Acao.DELETAR_AGENDAMENTO.label,
                        Acao.ABRIR_REPORTE.label, Acao.TROCAR_EQUIPAMENTO_SALA.label]
    context['alvo_acao'] = [TipoAlvo.ALUNO.label, TipoAlvo.ROOT.label, TipoAlvo.PROFESSOR.label,
                            TipoAlvo.ADMINISTRADOR.label, TipoAlvo.AGENDAMENTO.label, TipoAlvo.AR_CONDICIONADO.label,
                            TipoAlvo.COMPUTADOR.label, TipoAlvo.PREDIO.label, TipoAlvo.PROJETOR.label,
                            TipoAlvo.SALA.label, TipoAlvo.SETOR.label]
    context['objetos'] = [
        {'auditoria_id': '1', 'tipo_autor': TipoUsuario.TECNICO_TI, 'autor': 'joao@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reportes', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': TipoUsuario.TECNICO_TI, 'autor': 'joao@escolar.educ.br',
         'acao': 'Criar reporte',
         'alvo_acao': 'Reportes', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': TipoUsuario.TECNICO_TI, 'autor': 'joao@escolar.educ.br',
         'acao': 'Criar reporte',
         'alvo_acao': 'Reportes', 'data': date.today()},
        {'auditoria_id': '1', 'tipo_autor': TipoUsuario.TECNICO_TI, 'autor': 'joao@escolar.educ.br',
         'acao': 'Criar reporte',
         'alvo_acao': 'Reportes', 'data': date.today()},   {'auditoria_id': '1', 'tipo_autor': TipoUsuario.TECNICO_TI, 'autor': 'joao@escolar.educ.br', 'acao': 'Criar reporte',
         'alvo_acao': 'Reportes', 'data': date.today()},
    ]
    return HttpResponse(render(request, 'auditoria/paginas/auditoria.html', context))