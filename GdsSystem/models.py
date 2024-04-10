from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Projeto(models.Model):

    titulo = models.CharField(max_length=255, default=None, null=True, blank=True)
    descricao = models.CharField(max_length=255, default=None, null=True, blank=True)
    imagem = models.FileField(default=None, null=True, blank=True)
    grau = models.CharField(max_length=255, default=None, null=True, blank=True)
    serie = models.CharField(max_length=255, default=None, null=True, blank=True)
    disciplina = models.CharField(max_length=255, default=None, null=True, blank=True)
    local = models.CharField(max_length=255, default=None, null=True, blank=True)
    tipo = models.CharField(max_length=255, default=None, null=True, blank=True)
    estilo = models.CharField(max_length=255, default=None, null=True, blank=True)
    interesse = models.CharField(max_length=255, default=None, null=True, blank=True)
    habilidade = models.CharField(max_length=255, default=None, null=True, blank=True)
    recompensa = models.CharField(max_length=255, default=None, null=True, blank=True)
    competicao = models.CharField(max_length=255, default=None, null=True, blank=True)
    recurso = models.CharField(max_length=255, default=None, null=True, blank=True)
    limitacao = models.CharField(max_length=255, default=None, null=True, blank=True)
    tema = models.CharField(max_length=255, default=None, null=True, blank=True)
    problema = models.CharField(max_length=255, default=None, null=True, blank=True)
    regra = models.CharField(max_length=255, default=None, null=True, blank=True)
    detalhe = models.CharField(max_length=255,)
    historia = models.CharField(max_length=255, default=None, null=True, blank=True)
    vilao = models.CharField(max_length=255, default=None, null=True, blank=True)
    enredo = models.CharField(max_length=255, default=None, null=True, blank=True)
    emboscada = models.BooleanField(null=True, blank=True)
    feridos = models.BooleanField(null=True, blank=True)
    acontecimento = models.CharField(max_length=255, default=None, null=True, blank=True)
    objetivo = models.CharField(max_length=255, default=None, null=True, blank=True)
    falha = models.CharField(max_length=255, default=None, null=True, blank=True)
    desafio = models.CharField(max_length=255, default=None, null=True, blank=True)
    desafio_para_casa = models.CharField(max_length=255, default=None, null=True, blank=True)
    exercicio_em_equipe = models.CharField(max_length=255, default=None, null=True, blank=True)
    distintivo = models.CharField(max_length=255, default=None, null=True, blank=True)
    insignias = models.CharField(max_length=255, default=None, null=True, blank=True)
    item_secreto = models.CharField(max_length=255, default=None, null=True, blank=True)
    mecanica = models.CharField(max_length=255, default=None, null=True, blank=True)
    perigo = models.CharField(max_length=255, default=None, null=True, blank=True)
    problema_final = models.CharField(max_length=255, default=None, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    criado_em = models.DateField(auto_now_add=True)
    likes = models.IntegerField(null=True, blank=True, default=0)
    visualizacoes = models.IntegerField(null=True, blank=True, default=0)

    @staticmethod
    def fields_to_create():
        return [
            f.name
            for f in Projeto._meta.fields + Projeto._meta.many_to_many
            if 'id' != f.name
            and 'criado_em' != f.name
            and 'usuario' != f.name
            and 'likes' != f.name
            and 'visualizacoes' != f.name
        ]


class Perfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projetos_salvos = models.ManyToManyField(Projeto, blank=True)
    criado_em = models.DateField(auto_now_add=True)


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
