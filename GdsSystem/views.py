from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from GdsSystem.models import Projeto
from django.db.models import Q

class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjetoApi(APIView):

    def get(self, request, pk=None):
        username = pk if pk else request.user.username
        search = request.data.get('search')
        query = Q(usuario__username=username)
        if search:
            query &= (Q(titulo__contains=search) | Q(descricao__contains=search))
        projeto = Projeto.objects.filter(query)
        if not projeto.exists():
            return Response({'error': 'No project founded'})
        projeto = projeto.values()[0]
        return Response(projeto)

    def post(self, request, pk=None):
        if not all([field in request.data for field in Projeto.fields()]):
            return Response({'error': 'Invalid fields'})
        projeto = Projeto(**request.data)
        projeto.save()
        return Response({'novo_projeto': projeto.id})
