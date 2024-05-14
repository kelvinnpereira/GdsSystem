from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Projeto(models.Model):

    titulo = models.CharField(max_length=255, default=None, null=True, blank=True)
    descricao = models.TextField(default=None, null=True, blank=True)
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
            and 'descricao' != f.name
        ]

    @staticmethod
    def options_description():
        return {
            'tema': 'Tema do mundo: ',
            'mundo': 'O nome desse mundo: ',
            'historia_mundo': 'História do mundo: ',
            'era': 'O tempo em que se passa a história: ',
            'ambiente': 'Detalhes sobre o ambiente: ',
            'problema_ambiente': 'Problemas enfrentados:',
            'regra': 'Regra/Leis deste mundo: ',
            'detalhe': 'Detalhes pessoais, fisiológicos e outros que definam bem os jogadores: ',
            'historia_jogador': 'A história dos jogadores, por que estão ali?: ',
            'rotina': 'Sua rotina no mundo criado: ',
            'envolvimento': 'O tipo de envolvimento social que ocorre no mundo criado: ',
            'personagens_secundarios': 'Personagens secundários: ',
            'problema_jogador': 'Problemas enfrentados:',
            'hierarquias': 'Hierarquias: ',
            'vilao': 'Crie um vilão: ',
            'acontecimento': 'Algo que aconteceu fora do comum, ou planejado: ',
            'emboscada': 'Foi uma emboscada?: ',
            'feridos': 'Alguém saiu ferido ou sequestrado?: ',
            'viloes': 'Era um ou mais vilões?:',
            'plano_maligno': 'Tem um plano maligno?: ',
            'enredo': 'O que vai acontecer no mundo e com os jogadores?: ',
            'fim': 'É importante trabalhar o acontecimento até o fim da história: ',
            'herois': 'Quem pode auxiliar a resolver esses problemas? (Vamos chamar os heróis): ',
            'novo_mundo': 'Informe como será o novo mundo (caso ocorram modificações ou trocas): ',
            'objetivo': 'Qual o objetivo do jogador?: ',
            'desejos': 'Quais os seus maiores desejos, que o impulsionam para trilhar essa jornada?: ',
            'obstaculos': 'Os obstáculos que ele vai encontrar ao longo do caminho que está traçando rumo a seu objetivo?: ',
            'recompensa_jogo': 'Que tipos de recompensas ele pode encontrar pelo caminho?: ',
            'premio': 'Será premiado?: ',
            'segredo': 'Tem algum segredo envolvido na trama?: ',
            'jornada': 'A jornada vai ser longa?: ',
            'reconhecimento': 'As pessoas irão reconhecê-lo como um herói?: ',
            'item': 'Vai ter algo que o jogador vai recolher como item de colecionador?: ',
            'punicao': 'Existe algum tipo de punição?: ',
            'desafio': 'O Desafio Final: ',
        }


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
