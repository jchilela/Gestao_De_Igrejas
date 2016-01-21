# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Pais(models.Model):
	nomeDoPais = models.CharField(max_length=50)
	def __unicode__(self):
		return unicode(self.nomeDoPais)

class Provincia(models.Model):
	nomeDaProvincia = models.CharField(max_length=50)
	idDoPais = models.ForeignKey(Pais)

	def __unicode__(self):
		return unicode(self.nomeDaProvincia)

class Municipio(models.Model):
	nomeDoMunicipio = models.CharField(max_length=50)
	idDaProvincia = models.ForeignKey(Provincia)

	def __unicode__(self):
		return unicode(self.nomeDoMunicipio)

		
class Igreja(models.Model):
	nomeDaIgreja = models.CharField(max_length=100)
	endereco = models.CharField(max_length=50)
	bairro = models.CharField(max_length=50)
	cidade = models.ForeignKey(Municipio)
	provincia = models.ForeignKey(Provincia)
	caixaPostal = models.CharField(max_length=10)
	telefone = models.CharField(max_length=20)
	email = models.EmailField(max_length=200)
	dataDeCriacao = models.DateField()
	logotipo = models.ImageField(upload_to = 'fotos/', default = 'fotos/no-img.jpg')

	def __unicode__(self):
		return unicode(self.nomeDaIgreja)



class Departamento(models.Model):
	nomeDoDepartamento = models.CharField(max_length=50)
	idDaIgreja = models.ForeignKey(Igreja)

	def __unicode__(self):
		return unicode(self.nomeDoDepartamento)



class Membro(models.Model):
	nomeDoMembro = models.CharField(max_length=100)
	estadoCivil = models.CharField(max_length=20)
	sexo = models.CharField(max_length=10)
	cargo = models.CharField(max_length=50)
	funcaoNaIgreja= models.CharField(max_length=50)
	endereco = models.CharField(max_length=50)
	bairro = models.CharField(max_length=50)
	provincia = models.ForeignKey(Provincia)
	caixaPostal = models.CharField(max_length=10)
	telefone = models.CharField(max_length=20)
	email = models.EmailField(max_length=200)
	dataDeNascimento = models.DateField()
	#naturalidade = models.ForeignKey(Municipio)
	pais = models.ForeignKey(Pais)
	grauAcademico = models.CharField(max_length=50)
	profissao = models.CharField(max_length=50)
	numeroDeIdentificacao = models.CharField(max_length=50)
	conjuge = models.CharField(max_length=100)
	filiacaoPai = models.CharField(max_length=100)
	filiacaoMae = models.CharField(max_length=100)
	dataDeConversao = models.DateField(null=True,blank=True)
	procedencia = models.CharField(max_length=100)
	formaDeAdmissao = models.CharField(max_length=50)
	dataDeBaptismo = models.DateField(null=True,blank=True)
	localDeBaptismo = models.CharField(max_length=50,null=True,blank=True)
	dataDeConsagracaoDiacono = models.DateField(null=True,blank=True)
	dataDeConsagracaoEvangelista = models.DateField(null=True,blank=True)
	dataDeConsagracaoPastor = models.DateField(null=True,blank=True)
	dataDeConsagracaoMissionario = models.DateField(null=True,blank=True)
	departamento = models.ForeignKey(Departamento)
	igreja = models.ForeignKey(Igreja)
	numeroDeMembro= models.CharField(max_length=20)
	data = models.DateField()
	foto = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)

	def __unicode__(self):
		return unicode(self.nomeDoMembro)


class Dizimo(models.Model):
	nomeDoMembro = models.ForeignKey(Membro)
	igreja = models.ForeignKey(Igreja)
	valorDoDizimo = models.FloatField(default=None)
	dataDoDizimo = models.DateField()
	mesDoDizimo = models.CharField(max_length=20)
	anoDoDizimo=models.CharField(max_length=10)

	def __unicode__(self):
		return unicode(self.valorDoDizimo)


class Projeto(models.Model):
	igreja = models.ForeignKey(Igreja)
	descricaoDoProjeto = models.CharField(max_length=300)
	orcamento = models.FloatField(default=None)

	def __unicode__(self):
		return unicode(self.descricaoDoProjeto)


class Contribuicao(models.Model):
	nomeDoMembro = models.ForeignKey(Membro)
	igreja = models.ForeignKey(Igreja)
	valorDaContribuicao = models.FloatField(default=None)
	descricaoDaContribuicao = models.ForeignKey(Projeto)
	dataDaContribuicao = models.DateField()
	mesDaContribuicao = models.CharField(max_length=20)
	anoDaContribuicao = models.CharField(max_length=10)

	def __unicode__(self):
		return unicode(self.descricaoDaContribuicao)



class Oferta(models.Model):
	igreja = models.ForeignKey(Igreja)
	valorDaOferta = models.FloatField(default=None)
	dataDaOferta = models.DateField()
	mesDaOferta = models.CharField(max_length=20)
	anoDaOferta = models.CharField(max_length=10)

	def __unicode__(self):
		return unicode(self.valorDaOferta)


#Modulo recursos humanos
class Funcionario(models.Model):
	nomeDoFuncionario = models.CharField(max_length=100)
	estadoCivil = models.CharField(max_length=20)
	sexo = models.CharField(max_length=10)
	cargo = models.CharField(max_length=50)
	endereco = models.CharField(max_length=50)
	bairro = models.CharField(max_length=50)
	provincia = models.ForeignKey(Provincia)
	caixaPostal = models.CharField(max_length=10)
	telefone = models.CharField(max_length=20)
	email = models.EmailField(max_length=200)
	dataDeNascimento = models.DateField()
	#naturalidade = models.ForeignKey(Municipio)
	pais = models.ForeignKey(Pais)
	grauAcademico = models.CharField(max_length=50)
	profissao = models.CharField(max_length=50)
	numeroDeIdentificacao = models.CharField(max_length=50)
	filiacaoPai = models.CharField(max_length=100)
	filiacaoMae = models.CharField(max_length=100)
	numeroDeFuncionario= models.CharField(max_length=20)
	salarioBase = models.FloatField(default=None)
	foto = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)

	def __unicode__(self):
		return unicode(self.nomeDoFuncionario)


class Salario(models.Model):
	nomeDoFuncionario=models.ForeignKey(Funcionario)
	salarioAno = models.CharField(max_length=10)
	salarioMes= models.CharField(max_length=20)
	salarioSS = models.FloatField(default=None)
	salarioIRT = models.FloatField(default=None)
	salarioNumerodeFaltas = models.CharField(max_length=10)
	salarioBonus = models.FloatField(max_length=100)
	salarioLiquido = models.FloatField(default=None)

	def __unicode__(self):
		return unicode(self.salarioLiquido)



class Equipamento(models.Model):
    igreja = models.ForeignKey(Igreja)
    nome=models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    numeroDeSerie = models.CharField(max_length=30)
    dataDaAquisicao = models.DateField()
    modelo = models.CharField(max_length=30)
    localizacao = models.CharField(max_length=50)
    estado = models.CharField(max_length=30)
    preco = models.FloatField(default=None)
    obs = models.CharField(max_length=300)

    def __unicode__(self):
        return unicode(self.nome)


#NOTICIAS-----------------------------------------
class Noticias(models.Model):
    funcionario = models.ForeignKey(Membro)
    titulo = models.CharField(max_length=300)
    noticia=models.CharField(max_length=5000)
    foto = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
    dataPublicacao = models.DateField()
    tipo = models.CharField(max_length=20)
    def __unicode__(self):
        return unicode(self.titulo)

class Comentarios(models.Model):
    noticia=models.ForeignKey(Noticias)
    autor = models.CharField(max_length=100)
    comentario = models.CharField(max_length=5000)
    data = models.DateField()
    def __unicode__(self):
        return unicode(self.comentario)

class Eventos(models.Model):
    departamento = models.ForeignKey(Departamento)
    evento = models.CharField(max_length=5000)
    dataDoEvento = models.DateField()
    localDoEvento = models.CharField(max_length=200)
    igreja= models.ForeignKey(Igreja)
    autor = models.CharField(max_length=100)
    dataDaPublicacao = models.DateField()
    def __unicode__(self):
        return unicode(self.evento)


class Configuracoes(models.Model):
	igreja= models.ForeignKey(Igreja)
	imagem1 = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	imagem2 = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	texto1 = models.CharField(max_length=400)
	texto2 = models.CharField(max_length=400)
	texto3 = models.CharField(max_length=400)
	texto4 = models.CharField(max_length=400)
	texto5 = models.CharField(max_length=400)
	texto6 = models.CharField(max_length=400)
	desenvolvedores = models.CharField(max_length=200)
	def __unicode__(self):
		return unicode(self.desenvolvedores)


class Utilizador(models.Model):
	nomeDoMembro = models.ForeignKey(Membro)
	user = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __unicode__(self):
		return unicode(self.user)



class User(models.Model):
	funcionario = models.ForeignKey(Funcionario)
	userEmail = models.EmailField(max_length=100)
	userPassword = models.CharField(max_length=100)

	def __unicode__(self):
		return unicode(self.userEmail)

class Programa(models.Model):
	diaDaSemana=models.CharField(max_length=25)
	descricao=models.CharField(max_length=300)
	def __unicode__(self):
		return unicode(self.descricao)

