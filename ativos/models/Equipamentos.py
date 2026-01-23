from django.db import models
from core.essenciais import EstadoEquipamento, TipoEquipamento
from core.essenciais.Fileira import Fileira
from locais.models.Salas import Salas

from django.db.models import Count, F, Avg


class Equipamentos(models.Model):
    equipamento_id = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE, null=False, blank=False, related_name='equipamentos')
    posicao = models.IntegerField(null=False, blank=False)
    fileira = models.CharField(max_length=50, choices=Fileira.choices, null=False, blank=False)
    tipo = models.TextField(null=False, blank=False, choices=TipoEquipamento.choices)
    serial = models.CharField(null=False, unique=True, max_length=13)
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoEquipamento.choices, default=EstadoEquipamento.FUNCIONANDO, max_length=50)
    fabricante = models.CharField(null=False, blank=False, max_length=100)
    data_aquisicao = models.DateField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['posicao', 'fileira'], name='u_posicao_fileira')
        ]
        verbose_name = 'Equipamentos'
        verbose_name_plural = 'Equipamentos'

    def __srt__(self):
        return f'{self.tipo} / {self.serial}'

    @staticmethod
    def listar_equipamentos_mais_defeituosos_predio(predio_id):
        return Equipamentos.objects.filter(historico_manutencoes__equipamento__sala__setor__predio__predio_id=predio_id).values('equipamento_id', 'serial').annotate(manutencoes=Count('historico_manutencoes'), necessidade_substituicao=(Count('historico_manutencoes') * 100)/20).order_by('-manutencoes')

    @staticmethod
    def listar_equipamentos_mais_reincidencia_de_falhas_setor(setor_id):
        return Equipamentos.objects.filter(sala__setor__setor_id=setor_id, historico_manutencoes__equipamento__sala__setor__setor_id=setor_id).values('equipamento_id', 'tipo', 'serial', sala_localizacao=F('sala__localizacao')).annotate(manutencoes=Count('historico_manutencoes')).order_by('-manutencoes')

    @staticmethod
    def listar_equipamentos_do_predio(predio_id):
        return Equipamentos.objects.filter(sala__setor__predio__predio_id=predio_id)

    @staticmethod
    def listar_por_setor_sala_estado(setor_id, sala_id, estado:EstadoEquipamento):
        return Equipamentos.objects.filter(sala__sala_id=sala_id, sala__setor__setor_id=setor_id, estado_atual=estado.name)

    @staticmethod
    def listar_por_setor_sala(setor_id, sala_id):
        return Equipamentos.objects.filter(sala__sala_id=sala_id, sala__setor__setor_id=setor_id)

    @staticmethod
    def listar_por_sala_estado(sala_id, estado:EstadoEquipamento):
        return Equipamentos.objects.filter(sala__sala_id=sala_id, estado_atual=estado.name)

    @staticmethod
    def listar_por_setor_estado(setor_id, estado:EstadoEquipamento):
        return Equipamentos.objects.filter(sala__setor__setor_id=setor_id, estado_atual=estado.name)

    @staticmethod
    def listar_por_setor(setor_id):
        return Equipamentos.objects.filter(sala__setor__setor_id=setor_id)

    @staticmethod
    def listar_por_sala(sala_id):
        return Equipamentos.objects.filter(sala__sala_id=sala_id)

    @staticmethod
    def listar_por_estado(estado:EstadoEquipamento):
        return Equipamentos.objects.filter(estado_atual=estado.name)

    @staticmethod
    def listar_equipamentos_da_sala(sala_id):
        return Equipamentos.objects.filter(sala__sala_id=sala_id).order_by('posicao')

    @staticmethod
    def carregar(equipamento_id):
        return Equipamentos.objects.get(equipamento_id=equipamento_id)

    @staticmethod
    def listar_equipamentos():
        return Equipamentos.objects.all()