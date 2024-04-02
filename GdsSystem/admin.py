from django.contrib import admin
from GdsSystem.models import Projeto


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    pass
