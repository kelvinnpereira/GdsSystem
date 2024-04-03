from django.contrib import admin
from GdsSystem.models import Projeto, Perfil


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    pass


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    filter_horizontal = ['projetos_salvos']
