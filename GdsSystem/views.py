from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from GdsSystem.models import Projeto, Perfil, Comentario
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
import os
import json
import requests


class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PerfilAPI(APIView):

    def get(self, request, pk=None):
        perfil = Perfil.objects.filter(usuario=request.user)
        if not perfil.exists():
            return Response({'error': 'Perfil não encontrado'})
        usuario = model_to_dict(request.user)
        return Response({
            'data': {
                **perfil.values()[0],
                **usuario,
                'projetos': [
                    {
                        **model_to_dict(projeto, exclude=['comentarios']),
                        'usuario': projeto.usuario.username,
                        'imagem': projeto.imagem.name,
                    }
                    for projeto in Projeto.objects.filter(usuario=request.user).order_by('-id')
                ],
                'projetos_salvos': [
                    {
                        **model_to_dict(projeto),
                        'usuario': projeto.usuario.username,
                        'imagem': projeto.imagem.name,
                    }
                    for projeto in perfil.first().projetos_salvos.all().order_by('-id')
                ],
                'seguindo': perfil.first().seguindo.all().values(),
                'seguidores': perfil.first().seguidores.all().values(),
            }
        })

    def salvar_projeto(self, request, pk=None):
        perfil = Perfil.objects.get(usuario=request.user)
        projeto_id = int(pk)
        projeto = Projeto.objects.filter(~Q(usuario=request.user) & Q(id=projeto_id))
        if not projeto.exists():
            return Response({'error': 'Projeto não encontrado ou o projeto pertence ao usuario'})
        perfil.projetos_salvos.add(projeto_id)
        return Response({'data': f'Projeto ({projeto_id}) salvo com sucesso'})

    def curtir_projeto(self, request, pk=None):
        projeto_id = int(pk)
        projeto = Projeto.objects.filter(id=projeto_id)
        if not projeto.exists():
            return Response({'error': 'Projeto não encontrado'})
        projeto.curtidas.add(request.user)
        return Response({'data': f'Projeto ({projeto_id}) curtido com sucesso'})

    def comentar_projeto(self, request, pk=None):
        projeto_id = int(pk)
        projeto = Projeto.objects.filter(id=projeto_id)
        if not projeto.exists():
            return Response({'error': 'Projeto não encontrado'})
        Comentario.objects.create(
            usuario=request.user,
            projeto_id=projeto_id,
            comentario=request.data['comentario']
        )
        return Response({'data': f'Comentario no Projeto ({projeto_id}) realizado com sucesso'})

    def put(self, request, pk=None):
        data = request.data
        if data.get('type') == 'salvar_projeto':
            return self.salvar_projeto(request, pk)
        elif data.get('type') == 'curtir_projeto':
            return self.curtir_projeto(request, pk)
        elif data.get('type') == 'comentar_projeto':
            return self.comentar_projeto(request, pk)
        return Response({})


class ProjetoAPI(APIView):

    def get(self, request, pk=None):
        if isinstance(pk, str) and pk.isnumeric():
            projeto = Projeto.objects.filter(id=int(pk))
            if not projeto.exists():
                return Response({'error': 'Projeto não encontrado'})
            projeto = projeto.first()
            return Response({
                'data': {
                    **model_to_dict(projeto),
                    'imagem': projeto.imagem.name,
                    'comentarios': [
                        {
                            'comentario': comentario.comentario,
                            'usuario': f'{comentario.usuario.first_name} {comentario.usuario.last_name}'
                        }
                        for comentario in list(projeto.comentarios.through.objects.all())
                    ]
                }
            })
        projetos = Projeto.objects.all().order_by('-id')
        search = request.data.get('search')
        if search:
            projetos = projetos.filter((Q(titulo__contains=search) | Q(descricao__contains=search)))
        projetos = projetos.select_related('usuario')
        projetos = [
            {
                **model_to_dict(projeto, exclude=['comentarios']),
                'usuario': projeto.usuario.username,
                'imagem': projeto.imagem.name,
            }
            for projeto in projetos
        ]
        return Response({'data': projetos})


class ProjetoUsuarioAPI(APIView):

    def get_project_description(self, data):
        headers = {
            'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
            'Content-Type': 'application/json'
        }
        options_description = Projeto.options_description()
        description = [
            f'{options_description[key]}: {data[key]}'
            for key in options_description
        ]
        description = "\n".join(description)
        req_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f'''Chatgpt com base nas respostas abaixo crie uma narrativa para esta gamificação, em estilo de roteiro tendo um início, o clímax da história, que é o ponto alto da narrativa com a tarefa mais difícil e o fim.

                        As respostas estão descritas a seguir:
    
                        {description}
    
                        Siga essa estrutura e seja breve, não enrole muito:
    
                        1. Introdução
                        Faça um parágrafo dando caracteristicas para esse mundo, pois é ele o palco de todos os
                        acontecimentos. O nome desse mundo? Histórico do mundo, O tempo em que se passa a história, Detalhes sobre o ambiente, Problemas enfrentados caso haja algum problema para enfrentar, Regra/Leis deste mundo.
    
                        2. Fale sobre o JOGADOR
    
                        Faça um parágrafo sobre Detalhes pessoais, fisiológicos e outros que definam bem os jogadores. contando a história dos jogadores, por que estão ali?,  Sua rotina no mundo criado, O tipo de envolvimento social que ocorre no mundo criado
    
                        3. Conte a trama
    
                        Neste parágrafo diga o que rolou de diferente, diga quem é o vilão (lembre-se de vincular a história do mundo, ele não precisa ser uma pessoa, pode ser um acontecimento também ou outra coisa que desestabilizou o mundo do herói). Algo que aconteceu fora do comum, ou planejado?  Foi uma emboscada? Alguém saiu ferido ou sequestrado? Era um ou mais vilões? Tem um plano maligno? O que vai acontecer no mundo e com os jogadores? É importante trabalhar o acontecimento até o fim da história. Quem pode auxiliar a resolver esses problemas? (Vamos chamar os heróis)
    
                        4. Chegou a hora de fazer a “Chamada” para missão.
    
                        Neste parágrafo Informe como será o novo mundo (caso ocorram modificações ou trocas). Qual o objetivo do jogador? Quais os seus maiores desejos, que o impulsionam para trilhar essa jornada? Os obstáculos que ele vai encontrar ao longo do caminho que está traçando rumo a seu objetivo?Que tipos de recompensas ele pode encontrar pelo caminho? Sera premiado? Tem algum segredo envolvido na trama? A jornada vai ser longa? As pessoas irão reconhece-lo como um herói? Como ele vai saber que está avançando e indo no caminho certo? Seria bom usar um mapa? Vai ter algo que o jogador vai recolher como item de colecionador? Existe algum tipo de punição? É importante deixar clara a progressão do jogador, mencionando sobre o que lhe espera no desafio final, fazendo analogia com a aplicação mais difícil de todas. Existe trabalho em equipe? Se for trabalhar com equipes, como você as formaria dentro dessa proposta? Mistura entre mais velhos e mais novos? Seria um balanceamento por algum tipo de nota? Ou divisão de grupos apenas por quantidade de participantes, escolhendo cada um de forma aleatória? Diga-nos a sua lógica.
    
                        5. Sobre pontuação:
    
                        - Pense em uma pontuação que envolva as avaliações, os ganhos e
                        comportamentos durante o percurso do jogador.
                        - Faça uma lista de emblemas, distintivos ou outras formas de pontuação que serão utlizados e seus nomes para esta gamificação de acordo com o tema.
                        - O que acontece se uma pessoa não cumprir uma missão? Tem como
                        recuperar esse ponto?
                        - Presença conta como ponto?
                        - Lembre-se de deixar clara a forma como os pontos são calculados. Ex:
                        Missões realizadas + Ganhos + Presença = Proximo Lvl de XP
    
                        6. Para a missão:
    
                        - Título da fase.
                        - Conteúdo de aprendizagem que será explorado
                        - Local onde ocorre.
                        - Envolvido externos.
                        - Inimigos presentes na fase.
                        - Descreva o problema (Caso exista).
                        - Descreva o objetivo do jogador.
                        - Defina a missão de acordo com o conteúdo de aprendizagem
                        - O que acontece se alguém não conseguir completar a missão?
                        - Uma missão não concluída pode ser substituída por outra forma de ganho
                        de pontos? Como a pessoa pode se redimir nesse caso?
                        - No mínimo 1 (um) desafio.
    
                        7.O Desafio Final - Esse é o momento onde os jogadores vão se deparar com o
                        maior dos obstáculos.
    
                        É PRECISO...
                        - Explorar o vilão ao máximo.
                        - Conectar a etapa com alguns elementos encontrados pela jornada do herói,
                        para gerar flashbacks.
                        - Fazer com que o jogador entenda que tudo que ele já viu durante a jornada deve
                        ser usado agora.
                        - Dar dicas sobre o que deve ser feito para poder vencer esta etapa. 
                        - A aula/conteúdo mais complexo deve ser aplicada neste estágio.
                        - Lembre-se de fazer com que o jogador utilize as habilidades que desenvolveu durante a
                        sua jornada
    
                        8. Analise as pontuações e parabenize os jogadores conforme o placar de classificação.
    
                        - É importante acompanhar o placar de pontos.
                        - Missões realizadas + Ganhos + Presença = XP
    
                        Você decide a premiação, seria a chance de se gabar? Quais as conquistas dos heróis lembrem que elas têm que estar ligadas a participação, conhecimento, cumprimento das missões.
    
                        9. Conclusão da História:
    
                        - Finalize a história, fale sobre como tudo voltou ao normal, ou como tudo mudou a partir das ações realizadas pelo jogador.'''
                }
            ],
        }
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            data=json.dumps(req_data),
        )
        if response.status_code == 200:
            res_data = response.json()
            return res_data['choices'][0]['message']['content']
        return None

    def get(self, request, pk=None):
        query = Q(usuario__username=pk if pk else request.user.username)
        search = request.data.get('search')
        if search:
            query &= (Q(titulo__contains=search) | Q(descricao__contains=search))
        projeto = Projeto.objects.filter(query)
        if not projeto.exists():
            return Response({'error': 'No project founded'})
        return Response({'data': projeto.values()})

    def post(self, request, pk=None):
        data = request.data.dict()
        descricao = self.get_project_description(data)
        if not descricao:
            return Response({'error': 'Não foi possivel criar a descrição do projeto com IA'})
        imagem = data['imagem']
        del data['imagem']
        obj_to_create = {
            'titulo': data['titulo'],
            'descricao': descricao,
            'imagem': imagem,
            'campos': data,
            'usuario': request.user,
        }
        try:
            projeto = Projeto.objects.create(**obj_to_create)
            return Response({'data': projeto.id})
        except:
            return Response({'error': 'Não foi possivel criar o projeto'})

    def put(self, request, pk=None):
        projeto = Projeto.objects.filter(id=int(pk))
        if not projeto.exists():
            return Response({'error': 'Id do projeto invalido ou não existe'})
        projeto = projeto.filter(usuario=request.user)
        if not projeto.exists():
            return Response({'error': 'O usuario atual não pode editar o projeto por não ser o dono'})
        data = request.data.dict()
        descricao = self.get_project_description(data)
        if not descricao:
            return Response({'error': 'Não foi possivel editar a descrição do projeto com IA'})
        imagem = data['imagem']
        del data['imagem']
        obj_to_update = {
            'titulo': data['titulo'],
            'descricao': descricao,
            'imagem': imagem,
            'campos': data,
        }
        try:
            projeto.update(**obj_to_update)
            return Response({'data': projeto.first().id})
        except:
            return Response({'error': 'Não foi possivel editar o projeto'})

    def delete(self, request, pk=None):
        projeto = Projeto.objects.filter(id=int(pk))
        if not projeto.exists():
            return Response({'error': 'Id do projeto invalido ou não existe'})
        projeto = projeto.filter(usuario=request.user)
        if not projeto.exists():
            return Response({'error': 'O usuario atual não pode excluir o projeto por não ser o dono'})
        try:
            projeto_model = projeto.first()
            message = f'Projeto ({projeto_model.id}) excluido com sucesso'
            projeto.delete()
            return Response({'data': message})
        except:
            return Response({'error': 'Não foi possivel excluir o projeto'})
