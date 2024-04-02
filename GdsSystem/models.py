from django.db import models
from django.contrib.auth.models import User


class Projeto(models.Model):
    GRAU = {
        None: '',
        'medio': 'Ensino Médio',
        'fundamental': 'Ensino Fundamental',
        'superior': 'Ensino Superior',
        'tecnico': 'Ensino Tecnico',
    }

    SERIE = {
        None: '',
        'serie_1': '1º Série',
        'serie_2': '2º Série',
        'serie_3': '3º Série',
        'serie_4': '4º Série',
        'serie_5': '5º Série',
        'serie_6': '6º Série',
        'serie_7': '7º Série',
        'serie_8': '8º Série',
        'serie_9': '9º Série',
        'ano_1': '1º Ano',
        'ano_2': '2º Ano',
        'ano_3': '3º Ano',
    }

    DISCIPLINA = {
        None: '',
        'fisica': 'Fisica',
        'quimica': 'Quimica',
        'matematica': 'Matematica',
    }

    ESTILO = {
        None: '',
        'visual': 'Visual',
        'auditivo': 'Auditivo',
        'cinestesico': 'Cinestesico',
        'leitura_escrita': 'Leitura e Escrita'
    }

    INTERESSE = {
        None: '',
        'tecnologia': 'Tecnologia',
        'arte_cultura': 'Arte E Cultura',
        'ciencia': 'Ciência',
        'esporte': 'Esporte e Atividades',
        'fisica': 'Fisica',
    }

    HABILIDADE = {
        None: '',
        'criatividade': 'Criatividade',
        'lideranca': 'Liderança',
        'colaboracao': 'Colaboração',
        'resiliencia': 'Resiliência',
    }

    RECOMPENSA = {
        None: '',
        'moedas_pontos': 'Moedas ou pontos',
        'avatares': 'Avatares personalizáveis',
        'niveis': 'Níveis ou rankings',
    }

    COMPETICAO = {
        None: '',
        'lideres': 'Líderes de placar ou tabelas de classificação',
        'desafios': 'Desafios cronometrados que testam a velocidade',
        'missoes': 'Missões ou tarefas especiais pontuam',
    }

    RECURSO = {
        None: '',
        'quadro': 'Quadro',
        'laboratorio': 'Laboratório de informática',
        'biblioteca': 'Biblioteca',
        'quadra': 'Quadra poliesportiva',
    }

    LIMITACAO = {
        None: '',
        'restricao': 'Restrição de tempo para implementar a gamificação durante as aulas',
        'limitacao': 'Limitações de acesso à internet ou dispositivos eletrônicos na sala de aula',
        'disponibilidade': 'Disponibilidade limitada de recursos financeiros',
    }

    TEMA = {
        None: '',
        'mediavel': 'Medieval',
        'floresta': 'Floresta Magica',
        'reino': 'Reino Encantado',
        'futurista': 'Futurista',
        'corrida': 'Corrida',
    }

    PROBLEMA = {
        None: '',
        'virus': 'Vírus Tecnológico',
        'corporacoes': 'Corporações Dominam',
        'inteligencia': 'Inteligência Artificial',
        'autonoma': 'Autonoma',
        'escassez': 'Escassez de Recursos',
        'naturais': 'Naturais',
    }

    REGRA = {
        None: '',
        'viagem': 'Viagem no Tempo Proibida',
        'biotecnologia': 'Biotecnologia',
        'clones': 'Clones Humanos',
        'leis': 'Leis da robótica',
        'exploracao': 'Exploração de IA',
    }

    DETALHE = {
        None: '',
        'cibernetico': 'Possuem implantes cibernéticos avançados',
        'genetico': 'Possui um código genético exclusivo',
        'especies': 'Podem pertencer a diferentes raças ou espécies alienígenas',
    }

    HISTORIA = {
        None: '',
        'voluntarios': 'Voluntários em um programa de exploração',
        'recrutados': 'Recrutados para participar de uma resistência',
        'cientistas': 'Ciêntistas que foram enviados para estudar',
    }

    VILAO = {
        None: '',
        'militar': 'Ex-militar Ciberneticamente',
        'ia': 'Superinteligência Artificial',
        'magnata': 'Magnata Corporativo Corrupto',
    }

    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    imagem = models.FileField()
    conteudo = models.CharField(max_length=255)
    grau = models.CharField(max_length=255, choices=GRAU)
    serie = models.CharField(max_length=255)
    disciplina = models.CharField(max_length=255)
    estilo = models.CharField(max_length=255)
    interesse = models.CharField(max_length=255)
    habilidade = models.CharField(max_length=255)
    recompensa = models.CharField(max_length=255)
    competicao = models.CharField(max_length=255)
    recurso = models.CharField(max_length=255)
    limitacao = models.CharField(max_length=255)
    tema = models.CharField(max_length=255)
    problema = models.CharField(max_length=255)
    regra = models.CharField(max_length=255)
    detalhe = models.CharField(max_length=255)
    historia = models.CharField(max_length=255)
    vilao = models.CharField(max_length=255)
    enredo = models.CharField(max_length=255)
    emboscada = models.BooleanField()
    feridos = models.BooleanField()
    objetivo = models.CharField(max_length=255)
    falha = models.CharField(max_length=255)
    desafio = models.CharField(max_length=255)
    desafio_para_casa = models.CharField(max_length=255)
    exercicio_em_equipe = models.CharField(max_length=255)
    distintivo = models.CharField(max_length=255)
    insignias = models.CharField(max_length=255)
    item_secreto = models.CharField(max_length=255)
    mecanica = models.CharField(max_length=255)
    periodos = models.CharField(max_length=255)
    problema_final = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    criado_em = models.DateField(auto_now_add=True)

    @staticmethod
    def fields():
        return [f.name for f in Projeto._meta.fields + Projeto._meta.many_to_many if 'id' not in f.name]


class Perfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projetos_salvos = models.ManyToManyField(Projeto)



