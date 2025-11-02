from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de locais funcionando!")
def salas(request):
    return HttpResponse("Página de salas funcionando!")

def setores(request):
    return HttpResponse("Página de setores funcionando!")

def predios(request):
    return HttpResponse("Página de prédios funcionando!")


# VIEWS QUE CRIEI PARA TESTAR RENDERIZACAO DE HEADER DAS PAGINAS DE SALAS, SETORES, PREDIOS, E PREDIOS COM SELECAO DE EQUIPAMENTOS E SALAS(se quiser, pode excluir)

# def index(request):
#     return HttpResponse(render(request,
#                                'core/pages/../core/templates/core/partials/partials_do_headers/filtro/filtro.html'))
#
# def salas(request):
#     return HttpResponse(render(request, 'locais/partials/headers/sala/sala_header.html'))
#
# def setores(request):
#     return HttpResponse(render(request, 'locais/partials/headers/setor/setor_header.html/'))
#
# def predios(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_header.html'))
#
# def predios_equipamentos(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_equipamentos_header.html', {'setor': ['Administrativo', 'Acadêmico', 'Técnico'], 'sala': ['A17', 'A13', 'B24', 'C54', 'D2'], 'estado': [EstadoEquipamento.FUNCIONANDO, EstadoEquipamento.MANUTENCAO, EstadoEquipamento.DEFEITUOSO]}))
#
# def predios_salas(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_salas_header.html', {'setor': ['Administrativo', 'Acadêmico', 'Técnico'], 'sala': ['A17', 'A13', 'B24', 'C54', 'D2'], 'estado': [EstadoSala.LIBERADA, EstadoSala.MANUTENCAO, EstadoSala.INAPTA]}))