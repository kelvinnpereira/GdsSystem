from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Projeto(models.Model):

    titulo = models.CharField(max_length=255, default=None, null=True, blank=True)
    descricao = models.TextField(default=None, null=True, blank=True)
    imagem = models.FileField(default=None, null=True, blank=True)
    campos = models.JSONField(default=dict)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='usuario_set')
    criado_em = models.DateField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, blank=True, related_name='curtidas_set')
    visualizacoes = models.ManyToManyField(User, blank=True, related_name='visualizacoes_set')
    comentarios = models.ManyToManyField(User, blank=True, through='Comentario', related_name='comentarios_set')

    @staticmethod
    def options_description():
        return {
            'conteudo': 'Descreva sobre o conteúdo que será aprendido nesta missão?',
            'avaliacao': 'Qual será o tipo de avaliação?',
            'desafios': 'Quais tipos de desafios você gostaria de incluir?',
            'interacao': 'Como os participantes interagirão entre si e com o sistema de gamificação?',
            'recompensa': 'Que tipo de recompensas motivariam os participantes nesta missão?',
            'desempenho': 'Como será feita a avaliação do desempenho dos participantes na gamificação?',
            'feedback': 'Como os participantes receberão feedback durante a gamificação?',
            'falha': 'O que acontece se alguém não conseguir completar a missão?',
            'objetivo': 'O que você pretende alcançar com esta gamificação?',
            'planejamento': 'O que você planeja gamificar?',
            'duracao': 'Qual a duração estimada da gamificação? (em minutos, horas, dias)',
            'assunto': 'Qual o assunto que deseja que aprendam?',
            'local': 'Onde a gamificação será realizada?',
            'pessoas': 'Quantas pessoas participarão da atividade gamificada?',
            'idade': 'Qual a faixa etária dos participantes?',
            'perfil': 'Qual é o perfil dos participantes, o que eles gostam?',
            'tema': 'Tema principal da gamificação',
            'personalizar': 'Os participantes terão a oportunidade de personalizar suas experiências na gamificação?',
            'titulo': 'Titulo',
        }


class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    comentario = models.TextField(default=None, null=True, blank=True)


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
