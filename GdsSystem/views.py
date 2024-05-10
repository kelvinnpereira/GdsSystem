from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from GdsSystem.models import Projeto, Perfil
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


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
                        **model_to_dict(projeto),
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

    def put(self, request, pk=None):
        data = request.data
        if data.get('type') == 'salvar_projeto':
            return self.salvar_projeto(request, pk)
        return Response({})


class ProjetoAPI(APIView):

    def get(self, request, pk=None):
        if isinstance(pk, str) and pk.isnumeric():
            projeto = Projeto.objects.filter(id=int(pk))
            if not projeto.exists():
                return Response({'error': 'Projeto não encontrado'})
            return Response({'data': projeto.values()[0]})
        projetos = Projeto.objects.all().order_by('-id')
        search = request.data.get('search')
        if search:
            projetos = projetos.filter((Q(titulo__contains=search) | Q(descricao__contains=search)))
        paginator = Paginator(projetos, 100)
        page_obj = paginator.get_page(request.data.get('page_number', 1))
        projetos = [
            {
                **model_to_dict(projeto),
                'usuario': projeto.usuario.username,
                'imagem': projeto.imagem.name,
            }
            for projeto in page_obj.object_list.select_related('usuario')
        ]
        return Response({'data': projetos})


class ProjetoUsuarioAPI(APIView):

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
        if not all([field in data for field in Projeto.fields_to_create()]):
            return Response({'error': 'Missing or Invalid fields'})
        obj_to_create = {
            **data,
            'emboscada': bool(data['emboscada']),
            'feridos': bool(data['feridos']),
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
        if not all([field in data for field in Projeto.fields_to_create()]):
            return Response({'error': 'Existem campos invalidos ou faltando'})
        obj_to_create = {
            **data,
            'emboscada': bool(data['emboscada']),
            'feridos': bool(data['feridos']),
            'usuario': request.user,
        }
        try:
            projeto.update(**obj_to_create)
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
