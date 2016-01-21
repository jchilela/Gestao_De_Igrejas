#!/usr/bin/python
# -*- coding: latin-1 -*-

from django import forms
from django import forms
from .models import Pais, Provincia, Municipio, Igreja, Departamento, Membro, Oferta, Projeto, Dizimo, Contribuicao, Salario, Funcionario, Equipamento, Noticias,Comentarios,Eventos, Utilizador, Configuracoes 
from django.db import connection


def dictfetchall(cursor):
	desc = cursor.description
	return [dict(zip([call[0] for call in desc],raw)) for raw in cursor.fetchall()]

def get_provincia():
	provincia_opcao = connection.cursor()
	provincia_opcao.execute("select nomeDaProvincia, id from DjangoOnIis_provincia");
	return provincia_opcao.fetchall()

def get_pais():
	pais_opcao = connection.cursor()
	pais_opcao.execute("select nomeDoPais,nomeDoPais from DjangoOnIis_pais");
	return pais_opcao.fetchall()


def get_departamento():
	departamento_opcao = connection.cursor()
	departamento_opcao.execute("select nomeDoDepartamento,nomeDoDepartamento from DjangoOnIis_departamento");
	return departamento_opcao.fetchall()


def get_igreja():
	igreja_opcao = connection.cursor()
	igreja_opcao.execute("select nomeDaIgreja, provincia_id from DjangoOnIis_igreja");
	return igreja_opcao.fetchall()

class MembroForm(forms.Form):
	
	nomeDoMembro = forms.CharField(max_length=100)
	estadoCivil = forms.CharField(max_length=20)
	sexo = forms.CharField(max_length=10)
	cargo = forms.CharField(max_length=50, required=False)
	funcaoNaIgreja = forms.CharField(max_length=50, required=False)
	endereco = forms.CharField(max_length=50, required=False)
	bairro = forms.CharField(max_length=50, required=False)
	provincia = forms.CharField()
	caixaPostal = forms.CharField(max_length=10, required=False)
	telefone = forms.CharField(max_length=20, required=False)
	email = forms.EmailField(max_length=200, required=False)
	dataDeNascimento = forms.DateField()
	pais = forms.CharField()
	grauAcademico = forms.CharField(max_length=50, required=False)
	profissao = forms.CharField(max_length=50, required=False)
	numeroDeIdentificacao = forms.CharField(max_length=50)
	conjuge = forms.CharField(max_length=100, required=False)
	filiacaoPai = forms.CharField(max_length=100, required=False)
	filiacaoMae = forms.CharField(max_length=100, required=False)
	dataDeConversao = forms.DateField(required=False)
	procedencia = forms.CharField(max_length=100, required=False)
	formaDeAdmissao = forms.CharField(max_length=50, required=False)
	dataDeBaptismo = forms.DateField(required=False)
	localDeBaptismo = forms.CharField(max_length=50,required=False)
	dataDeConsagracaoDiacono = forms.DateField(required=False)
	dataDeConsagracaoEvangelista = forms.DateField(required=False)
	dataDeConsagracaoPastor = forms.DateField(required=False)
	dataDeConsagracaoMissionario = forms.DateField(required=False)
	departamento = forms.CharField()
	igreja = forms.CharField()
	numeroDeMembro = forms.CharField(max_length=20,required=False)
	data=forms.DateField(required=False)
	foto = forms.ImageField(label='Seleccionar imagem', required=False)

class DizimoForm(forms.Form):
	nomeDoMembro = forms.CharField(required=False)
	igreja = forms.CharField()
	valorDoDizimo = forms.FloatField()
	dataDoDizimo = forms.DateField()
	mesDoDizimo = forms.CharField()
	anoDoDizimo = forms.CharField()

class ContribuicaoForm(forms.Form):
	nomeDoMembro = forms.CharField()
	igreja = forms.CharField()
	valorDaContribuicao = forms.FloatField()
	descricaoDaContribuicao = forms.CharField()
	dataDaContribuicao = forms.DateField()
	mesDaContribuicao = forms.CharField()
	anoDaContribuicao = forms.CharField()

class OfertaForm(forms.Form):
	igreja = forms.CharField()
	valorDaOferta = forms.FloatField()
	dataDaOferta = forms.DateField()
	mesDaOferta = forms.CharField()
	anoDaOferta = forms.CharField()


class ProjetoForm(forms.Form):
	igreja = forms.CharField()
	descricaoDoProjeto = forms.CharField()
	orcamento = forms.FloatField()


class FuncionarioForm(forms.Form):
	nomeDoFuncionario = forms.CharField(max_length=100)
	estadoCivil = forms.CharField(max_length=20)
	sexo = forms.CharField(max_length=10)
	cargo = forms.CharField(max_length=50, required=False)
	endereco = forms.CharField(max_length=50, required=False)
	bairro = forms.CharField(max_length=50, required=False)
	provincia = forms.ChoiceField(choices=get_provincia(),required=False)
	caixaPostal = forms.CharField(max_length=10, required=False)
	telefone = forms.CharField(max_length=20, required=False)
	email = forms.EmailField(max_length=200, required=False)
	dataDeNascimento = forms.DateField()
	pais = forms.ChoiceField(choices=get_pais())
	grauAcademico = forms.CharField(max_length=50, required=False)
	profissao = forms.CharField(max_length=50, required=False)
	numeroDeIdentificacao = forms.CharField(max_length=50)
	filiacaoPai = forms.CharField(max_length=100, required=False)
	filiacaoMae = forms.CharField(max_length=100, required=False)
	numeroDeFuncionario = forms.CharField(max_length=20, required=False)
	salarioBase = forms.FloatField(required=False)
	foto = forms.ImageField(label='Seleccionar imagem', required=False)


class SalarioForm(forms.Form):
	nomeDoFuncionario=forms.CharField()
	salarioAno = forms.CharField()
	salarioMes= forms.CharField()
	salarioSS = forms.FloatField(required=False)
	salarioIRT = forms.FloatField(required=False)
	salarioNumerodeFaltas = forms.CharField(required=False)
	salarioBonus = forms.FloatField(required=False)
	salarioLiquido = forms.FloatField(required=False)

class EquipamentoForm(forms.Form):
    igreja = forms.CharField()
    nome=forms.CharField()
    marca = forms.CharField()
    numeroDeSerie = forms.CharField(required=False)
    dataDaAquisicao = forms.DateField(required=False)
    modelo = forms.CharField(required=False)
    localizacao = forms.CharField()
    estado = forms.CharField()
    preco = forms.FloatField(required=False)
    obs = forms.CharField(required=False)

class NoticiasForm(forms.Form):
    titulo = forms.CharField()
    noticia=forms.CharField()
    foto = forms.ImageField(label='Seleccionar imagem')
    funcionario=forms.CharField()
    dataPublicacao = forms.DateField(required=False)
    tipo = forms.CharField(required=False)


class ComentariosForm(forms.Form):
    noticia=forms.CharField()
    autor = forms.CharField()
    comentario = forms.CharField()
    data = forms.DateField(required=False)
    


class EventosForm(forms.Form):
    departamento = forms.CharField()
    evento = forms.CharField()
    dataDoEvento = forms.DateField()
    localDoEvento = forms.CharField(required=False)
    igreja= forms.CharField(required=False)
    autor = forms.CharField()
    dataDaPublicacao = forms.DateField()



class ConfiguracoesForm(forms.Form):
	igreja= forms.CharField()
	imagem1 = forms.ImageField(label='Seleccionar imagem')
	imagem2 = forms.ImageField(label='Seleccionar imagem',required=False)
	texto1 = forms.CharField()
	texto2 = forms.CharField(required=False)
	texto3 = forms.CharField(required=False)
	texto4 = forms.CharField(required=False)
	texto5 = forms.CharField(required=False)
	texto6 = forms.CharField(required=False)
	desenvolvedores = forms.CharField(required=False)


class PesquisarNoticiaForm(forms.Form):
	tipo = forms.CharField()
class ProgramaForm(forms.Form):
	diaDaSemana=forms.CharField(required=True)
	descricao=forms.CharField(required=True)


class UserForm(forms.Form):
	funcionario = forms.ChoiceField()
	userEmail = forms.ChoiceField()
	Userpassword = forms.ChoiceField()


class UsuariosForm(forms.Form):
	nomeDoMembro=forms.CharField()
        user = forms.CharField()
        password = forms.CharField()

class PesquisarHome_site(forms.Form):
	pesquisa = forms.CharField(required=True)
