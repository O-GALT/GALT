import qrcode
import socket
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core.essenciais import Acao, TipoAlvo
from locais.forms import UsuarioForm, PredioForm, SetorForm, SalaForm, EquipamentoForm
from core.emails.GerenciadorEmails import GerenciadorEmails
from django.contrib.auth import authenticate, login
from core.auditorias.GerenciadorAuditoria import GerenciadorAuditoria
from django.contrib import messages
from django.contrib.auth import authenticate, login


def pagina_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_escolar')
        password = request.POST.get('senha')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # limpa o email salvo temporariamente
            request.session.pop('email_temp', None)

            return redirect('/locais/predios/1/')  # ajuste para sua rota correta
        else:
            # salva email temporariamente para reaparecer no input
            request.session['email_temp'] = username

            # cria a mensagem de erro
            messages.error(request, 'Email ou senha incorretos.')

            # redirect é obrigatório para o messages funcionar bem
            return redirect('core_login')

    return render(request, 'core/pages/login.html')

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def concluido_modal(request):
    return render(request, 'core/pages/modais/modal-concluido.html')

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def exclusao_modal(request):
    return render(request, 'core/pages/modais/modal-exclusao.html')

def equipamento_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/equipamento-visao-usuario.html')

@login_required
def report_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/report-equipamento-usuario.html')


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_usuario_modal(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            admin = request.user

            user = form.save(commit=False)
            user.username = user.email_escolar
            user.nome = user.email_escolar
            password = user.password
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            GerenciadorEmails.enviar_email(user.email, user.email_escolar, password, user.groups)
            GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_USUARIO, list(user.groups.all())[0])
            return HttpResponseRedirect(reverse('criar_recursos'))
        else:
            print(form.errors)
            return HttpResponse('error')
    else:
        form = UsuarioForm()
    return render(request, 'core/pages/modais/modal-criar-usuario.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_predio_modal(request):
    form = PredioForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_PREDIO, TipoAlvo.PREDIO)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-predio.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_setor_modal(request):
    form = SetorForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_SETOR, TipoAlvo.SETOR)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-setor.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_sala_modal(request):
    form = SalaForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_SALA, TipoAlvo.SALA)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-sala.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_equipamento_modal(request):
    form = EquipamentoForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_EQUIPAMENTO, TipoAlvo(form.cleaned_data['tipo']))
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', {'form': form})

def gerar_qr_code(request, url):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # não envia nada
    ip = s.getsockname()[0]
    s.close()

    if ',' in url:
        url_splited = url.split(',')
        url = request.scheme + '://' + ip + ':8000' + reverse(url_splited[0], args=url_splited[1])
    else:
        url = request.scheme + '://' + ip + ':8000' + reverse(url)

    qr_code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4
    )

    qr_code.add_data(url)
    qr_code.make(fit=True)

    img = qr_code.make_image(
        fill_color='white',
        back_color='blue'
    )

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def exibir_qr_code(request, url):
    return HttpResponse(
        gerar_qr_code(request, url).getvalue(),
        content_type='image/png'
    )

def baixar_qr_code(request, url, identificador):
    return FileResponse(
        gerar_qr_code(request, url),
        as_attachment=True,
        filename= identificador + '_qrcode.png'
    )

def custom_page_not_found_view(request, exception):
    return render(request, 'core/pages/page_not_found/page_not_found.html', status=404)

def custom_permission_denied_view(request, exception):
    return render(request, 'core/pages/not_access/not_access.html', status=403)
