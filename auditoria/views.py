from datetime import date
from urllib.parse import urlencode

from django.shortcuts import render
from django.http import HttpResponse

from auditoria.models.AuditoriaLog import AuditoriaLog
from contas.models import Usuarios
from core.essenciais import TipoUsuario, Acao, TipoAlvo
from django.core.paginator import Paginator, Page

from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario


# Create your views here.

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def index(request):
    '''
    PARA LUCAS:
    A PARTE DA PAGINAÇÃO JÁ ESTÁ FUNCIONAL. VOCÊ DEVE SE PREOCUPAR APENAS EM
    FAZER A COMBINAÇÃO DOS FITLROS (JÁ TEM TODOS OS MÉTODOS NECESÁRIOS EM MODEL DE AUDITORIA PARA TU FAZER
    AS BUSCAS NO BANCO. SEU FOCO VAI SER EM IMPLEMENTAR ESSA LÓGICA EM IF'S ENCADEADOS UM ABAIXO DO OUTRO SEMPRE
    SETANDO UMA NOVA QUERY_SET. EU DEIXEI UM EXEMPLO QUE COMEÇA NA LINHA 36 QUE É QUANDO O USUARIO FAZ AS COMBINAÇÕES
    DE TODOS OS FILTROS JUNTOS. AO FINAL, QUANDO NÃO TIVER NENHUMA COMBINAÇÃO PARA FAZER DE FILTRO TU APENAS
    FAZ UMA SIMPLES LISTAGEM DE TUDO QUE ESTÁ NA AUDITORIA (JÁ TEM UM MÉTODO PARA ISSO NO MODEL DE AUDITORIA)

    NA LINHA 43 TEM UMA CONSULTA QUE FIZ QUE PEGA LOGO DE CARA TODAS AS AUDITORIAS, MAS NÃO EH PARA ELA ESTAR AÍ. EU SÓ FIL ISSO
    PARA NÃO ESTOURAR UM ERRO NA HORA QUE TU FOR ABRIR A PÁGINA DE AUDITORIAS. ESSA CONSULTA É PARA SER A ÚLTIMA,
    QUANDO NÃO TIVER NENHUM FILTRO SETADO. MAS ANTES DE TIRAR ELA, OLHA A PÁGINA DE AUDITORIA E DÁ UMA TESTADA

    '''
    query_set = None
    tipo_autor = request.GET.get('tipo_autor')
    autor = request.GET.get('autor')
    acao = request.GET.get('acao')
    alvo = request.GET.get('alvo_acao')

    
    if tipo_autor and autor and acao and alvo:
        query_set = AuditoriaLog.listar_por_tipo_autor_email_escolar_acao_alvo(TipoUsuario(tipo_autor), autor, Acao(acao), TipoAlvo(alvo))

    elif tipo_autor and autor:
        query_set = AuditoriaLog.listar_por_tipo_autor_email_escolar_acao(TipoUsuario(tipo_autor), autor, Acao(acao))

    elif tipo_autor and acao:
        query_set = AuditoriaLog.listar_por_tipo_autor_email_escolar(TipoUsuario(tipo_autor), autor)

    elif tipo_autor and alvo:
        query_set = AuditoriaLog.listar_por_tipo_autor_alvo(TipoUsuario(tipo_autor), TipoAlvo(alvo))

    elif autor and acao:
        query_set = AuditoriaLog.listar_por_email_escolar_acao(TipoUsuario(tipo_autor), Acao(acao))

    elif autor and alvo:
        query_set = AuditoriaLog.listar_por_email_escolar_alvo(autor, TipoAlvo(alvo))

    elif acao and alvo:
        query_set = AuditoriaLog.listar_acao_alvo(Acao(acao), TipoAlvo(alvo))

    elif tipo_autor:
        query_set = AuditoriaLog.listar_por_tipo_autor(TipoUsuario(tipo_autor))

    elif autor:
        query_set = AuditoriaLog.listar_por_email_escolar(autor)

    elif acao:
        query_set = AuditoriaLog.listar_por_acao(Acao(acao))

    elif alvo:
        query_set = AuditoriaLog.listar_por_alvo_acao(TipoAlvo(alvo))
    
    else:
        query_set = AuditoriaLog.listar_auditorias()

    paginator = Paginator(query_set, 7)
    page_obj: Page

    query_string = request.GET.copy()
    if request.GET.get('page'):
        page_obj = paginator.get_page(request.GET.get('page'))
        query_string.pop('page')
    else:
        page_obj = paginator.get_page(1)


    # tem_pagina = page_obj.has_next()
    # proxima = page_obj.next_page_number()
    context = {}
    context['query_string'] = urlencode(query_string)
    context['tipo_autores'] = [{'input': tipo.name, 'output': tipo.label} for tipo in [tipo_autor for tipo_autor in TipoUsuario]]
    context['autores'] = [{'input': usuario.email_escolar, 'output': usuario.email_escolar} for usuario in Usuarios.listar_usuarios()]
    context['acoes'] = [{'input': acao.name, 'output': acao.label} for acao in [tipo_acao for tipo_acao in Acao]]
    context['alvo_acao'] = [{'input': alvo.name, 'output': alvo.label} for alvo in [tipo_alvo for tipo_alvo in TipoAlvo]]
    context['page_obj'] = page_obj
    context['objetos'] = [{'auditoria_id': pagina.auditoria_id, 'tipo_autor': pagina.usuario.groups.all()[0], 'autor': pagina.usuario.email_escolar, 'acao': pagina.acao, 'alvo_acao': pagina.alvo_acao, 'data': pagina.data} for pagina in page_obj]

    return HttpResponse(render(request, 'auditoria/paginas/auditoria.html', context))