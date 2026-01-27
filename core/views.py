import qrcode
import socket
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ativos.models import Equipamentos
from auditoria.models import AuditoriaLog
from contas.models import TecnicosTI
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario, EstadoEquipamento, TipoEquipamento, Fileira

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.essenciais import Acao, TipoAlvo
from core.essenciais.EstadoReporte import EstadoReporte
from locais.forms import UsuarioForm, PredioForm, SetorForm, SalaForm, EquipamentoForm
from core.emails.GerenciadorEmails import GerenciadorEmails
from django.contrib.auth import authenticate, login
from core.auditorias.GerenciadorAuditoria import GerenciadorAuditoria
from django.contrib import messages
from django.contrib.auth import authenticate, login

from suporte.models import Reportes

from locais.models import Predios, Salas, Setores
from ativos.models import Equipamentos


def pagina_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('email_escolar'),
            password=request.POST.get('senha')
        )

        if user:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        return render(request, 'core/pages/login.html')

    return render(request, 'core/pages/login.html')

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def concluido_modal(request):
    return render(request, 'core/pages/modais/modal-concluido.html')

@login_required
def exclusao_modal(request):
    return render(request, 'core/pages/modais/modal-exclusao.html')

def equipamento_visao_usuario(request, equipamento_id):
    equipamento: Equipamentos = Equipamentos.carregar(equipamento_id)
    context = {
        'equipamento': equipamento,
        'reportes_enviados': equipamento.reportes.filter(estado_atual=EstadoReporte.ABERTO.name).count(),
        'estado': EstadoEquipamento(equipamento.estado_atual).label,
        'tipo': TipoEquipamento(equipamento.tipo).label,
        'fileira': Fileira(equipamento.fileira).label,
        'manutencoes_realizadas': equipamento.historico_manutencoes.count()
    }

    if request.POST:
        Reportes(
            equipamento=equipamento,
            usuario=request.user,
            titulo=request.POST['title'],
            mensagem=request.POST['problem-description']
        ).save()
        equipamento.verificar_e_atualizar_estado_apos_reporte(request.user)
        AuditoriaLog.persistir_auditoria(request.user, Acao.ABRIR_REPORTE, TipoAlvo(equipamento.tipo))

    return render(request, 'core/pages/visao-do-usuario/equipamento-visao-usuario.html', context)

@login_required
def report_visao_usuario(request, equipamento_id):
    context = {
        'equipamento_id': equipamento_id
    }
    return render(request, 'core/pages/visao-do-usuario/report-equipamento-usuario.html', context)


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

            if user.groups.get(name=TipoUsuario.TECNICO_TI):
                tecnico = TecnicosTI(
                    usuario=user,
                    cargo='Profisional técnico'
                )
                tecnico.save()
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

def editar_equipamento_modal(request, equipamento_id):
    equipamento = get_object_or_404(Equipamentos, pk=equipamento_id)
    form = EquipamentoForm(request.POST or None, instance=equipamento)
    if form.is_valid():
        admin = request.user
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-editar-equipamento.html', {'form': form, 'equipamento': equipamento})

def editar_sala_modal(request, sala_id):
    sala = get_object_or_404(Salas, pk=sala_id)
    form = SalaForm(request.POST or None, instance=sala)
    if form.is_valid():
        admin = request.user
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-editar-sala.html', {'form': form, 'sala': sala})

def editar_predio_modal(request, predio_id):
    predio = get_object_or_404(Predios, pk=predio_id)
    form = PredioForm(request.POST or None, instance=predio)
    if form.is_valid():
        admin = request.user
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-editar-predio.html', {'form': form, 'predio': predio})

def editar_setor_modal(request, setor_id):
    setor = get_object_or_404(Setores, pk=setor_id)
    form = SetorForm(request.POST or None, instance=setor)
    if form.is_valid():
        admin = request.user
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-editar-setor.html', {'form': form, 'setor': setor})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def excluir_predio(request, predio_id):
    predio = get_object_or_404(Predios, predio_id=predio_id)

    if request.method == "POST":
        predio.delete()
        return redirect("home")

    return render(request, 'core/pages/modais/modal-exclusao-predio.html', {
        'predio': predio
    })

def excluir_setor(request, setor_id):
    setor = get_object_or_404(Setores, setor_id=setor_id)

    if request.method == "POST":
            setor.delete()
            return redirect("home")

    return render(request, 'core/pages/modais/modal-exclusao-setor.html', {
        'setor': setor
    })

def excluir_sala(request, sala_id):
    sala = get_object_or_404(Salas, sala_id=sala_id)

    if request.method == "POST":
            sala.delete()
            return redirect("home")

    return render(request, 'core/pages/modais/modal-exclusao-sala.html', {
        'sala': sala
    })

def excluir_equipamento(request, equipamento_id):
    equipamento = get_object_or_404(Equipamentos, equipamento_id=equipamento_id)

    if request.method == "POST":
            equipamento.delete()
            return redirect("home")

    return render(request, 'core/pages/modais/modal-exclusao-equipamento.html', {
        'objeto': equipamento
    })

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


