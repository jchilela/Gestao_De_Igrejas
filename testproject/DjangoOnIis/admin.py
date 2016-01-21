from django.contrib import admin
from .models import Pais,Provincia, Utilizador, Municipio,Igreja,Departamento,Membro,Programa, Configuracoes, Dizimo, Projeto, Oferta, Contribuicao, Salario, Funcionario,Noticias
# Register your models here.
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(Igreja)
admin.site.register(Departamento)
admin.site.register(Membro)
admin.site.register(Dizimo)
admin.site.register(Projeto)
admin.site.register(Oferta)
admin.site.register(Contribuicao)
admin.site.register(Salario)
admin.site.register(Funcionario)
admin.site.register(Programa)
admin.site.register(Noticias)
admin.site.register(Configuracoes)
admin.site.register(Utilizador)
