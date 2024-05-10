from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Projeto(models.Model):

    titulo = models.CharField(max_length=255, default=None, null=True, blank=True)
    descricao = models.CharField(max_length=255, default=None, null=True, blank=True)
    imagem = models.FileField(default=None, null=True, blank=True)
    grau = models.CharField(max_length=255, default=None, null=True, blank=True)
    disciplina = models.CharField(max_length=255, default=None, null=True, blank=True)
    local = models.CharField(max_length=255, default=None, null=True, blank=True)
    tipo = models.CharField(max_length=255, default=None, null=True, blank=True)
    estilo = models.CharField(max_length=255, default=None, null=True, blank=True)
    interesse = models.CharField(max_length=255, default=None, null=True, blank=True)
    habilidade = models.CharField(max_length=255, default=None, null=True, blank=True)
    recompensa_virtual = models.CharField(max_length=255, default=None, null=True, blank=True)
    competicao = models.CharField(max_length=255, default=None, null=True, blank=True)
    recurso = models.CharField(max_length=255, default=None, null=True, blank=True)
    limitacao = models.CharField(max_length=255, default=None, null=True, blank=True)
    tema = models.CharField(max_length=255, default=None, null=True, blank=True)
    mundo = models.CharField(max_length=255, default=None, null=True, blank=True)
    historia_mundo = models.CharField(max_length=255, default=None, null=True, blank=True)
    era = models.CharField(max_length=255, default=None, null=True, blank=True)
    ambiente = models.CharField(max_length=255, default=None, null=True, blank=True)
    problema_ambiente = models.CharField(max_length=255, default=None, null=True, blank=True)
    regra = models.CharField(max_length=255, default=None, null=True, blank=True)
    detalhe = models.CharField(max_length=255, default=None, null=True, blank=True)
    historia_jogador = models.CharField(max_length=255, default=None, null=True, blank=True)
    rotina = models.CharField(max_length=255, default=None, null=True, blank=True)
    envolvimento = models.CharField(max_length=255, default=None, null=True, blank=True)
    personagens_secundarios = models.CharField(max_length=255, default=None, null=True, blank=True)
    problema_jogador = models.CharField(max_length=255, default=None, null=True, blank=True)
    hierarquias = models.CharField(max_length=255, default=None, null=True, blank=True)
    vilao = models.CharField(max_length=255, default=None, null=True, blank=True)
    acontecimento = models.CharField(max_length=255, default=None, null=True, blank=True)
    emboscada = models.CharField(max_length=255, default=None, null=True, blank=True)
    feridos = models.CharField(max_length=255, default=None, null=True, blank=True)
    viloes = models.CharField(max_length=255, default=None, null=True, blank=True)
    plano_maligno = models.CharField(max_length=255, default=None, null=True, blank=True)
    enredo = models.CharField(max_length=255, default=None, null=True, blank=True)
    fim = models.CharField(max_length=255, default=None, null=True, blank=True)
    herois = models.CharField(max_length=255, default=None, null=True, blank=True)
    novo_mundo = models.CharField(max_length=255, default=None, null=True, blank=True)
    objetivo = models.CharField(max_length=255, default=None, null=True, blank=True)
    desejos = models.CharField(max_length=255, default=None, null=True, blank=True)
    obstaculos = models.CharField(max_length=255, default=None, null=True, blank=True)
    recompensa_jogo = models.CharField(max_length=255, default=None, null=True, blank=True)
    premio = models.CharField(max_length=255, default=None, null=True, blank=True)
    segredo = models.CharField(max_length=255, default=None, null=True, blank=True)
    jornada = models.CharField(max_length=255, default=None, null=True, blank=True)
    reconhecimento = models.CharField(max_length=255, default=None, null=True, blank=True)
    item = models.CharField(max_length=255, default=None, null=True, blank=True)
    punicao = models.CharField(max_length=255, default=None, null=True, blank=True)
    desafio = models.CharField(max_length=255, default=None, null=True, blank=True)
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
    bio = models.TextField(blank=True, null=True, default=None)
    cidade = models.CharField(max_length=255, default=None, null=True, blank=True)
    estado = models.CharField(max_length=255, default=None, null=True, blank=True)
    pais = models.CharField(max_length=255, default=None, null=True, blank=True)
    seguindo = models.ManyToManyField('self', blank=True)
    seguidores = models.ManyToManyField('self', blank=True)


@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
