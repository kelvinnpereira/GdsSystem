# Generated by Django 5.0.2 on 2024-04-03 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GdsSystem', '0002_perfil_criado_em_alter_projeto_competicao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='projetos_salvos',
            field=models.ManyToManyField(blank=True, to='GdsSystem.projeto'),
        ),
    ]
