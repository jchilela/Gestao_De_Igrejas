# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :
from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseRedirect
from .models import Pais,Provincia,Programa, Municipio, Igreja, Departamento,Utilizador, Membro,Dizimo,Contribuicao,Oferta,Projeto, Funcionario, Salario, User
#from .forms import IgrejaForm
from django.db import connection
from .forms import MembroForm,DizimoForm,ProgramaForm,ContribuicaoForm,ProjetoForm,OfertaForm, FuncionarioForm, SalarioForm, UserForm, PesquisarNoticiaForm
from datetime import date
from .forms import EquipamentoForm,UsuariosForm,PesquisarHome_site
from .models import Equipamento
from .forms import NoticiasForm,EventosForm,ComentariosForm
from .models import Noticias,Eventos,Comentarios,Configuracoes
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.pagesizes import landscape
import sys 
import time, datetime
from django.template import Template, Context
from django.template import RequestContext
reload(sys)  
sys.setdefaultencoding('utf8')

# View para inserir membros

def dictfetchall(cursor):
	desc = cursor.description
	return [dict(zip([call[0] for call in desc],raw)) for raw in cursor.fetchall()]

def provincia_pesquisa(opcao):
	provincia_opcao = connection.cursor()
	provincia_opcao.execute("select distinct (id) from DjangoOnIis_provincia where nomeDaProvincia='%s'" % opcao);
	return dictfetchall(provincia_opcao)

def lista_provincia():
	provincia_opcao = connection.cursor()
	provincia_opcao.execute("select distinct (id),nomeDaProvincia from DjangoOnIis_provincia");
	return dictfetchall(provincia_opcao)



def lista_pais():
	pais_opcao= connection.cursor()
	pais_opcao.execute("select nomeDoPais from DjangoOnIis_pais ");
	return dictfetchall(pais_opcao)


"""def inserirMembro(request):
	provincia = lista_provincia()
	pais = lista_pais
	departamento=Departamento.objects.all()
	igreja = Igreja.objects.all()

	return render(request, 'inserirMembros.html',{'provincia':provincia,'pais':pais,'departamento':departamento,'igreja':igreja})"""

def home(request):
        igreja = Igreja.objects.last()
        ano = datetime.date.today().year
        template = 'home.html'
        configuracoes = Configuracoes.objects.last()
        return render(request,template,{'igreja':igreja,'ano':ano,'configuracoes':configuracoes})
	
def homeMembro(request):
	try:
		if request.session['user']:
			if request.method == 'POST':
				form = MembroForm(request.POST , request.FILES)
				
				if form.is_valid():
					provincia = Provincia.objects.get(nomeDaProvincia=form.cleaned_data['provincia'])
					pais = Pais.objects.get(nomeDoPais=form.cleaned_data['pais'])
					departamento = Departamento.objects.get(nomeDoDepartamento=form.cleaned_data['departamento'])
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					nomeDoMembro = form.cleaned_data['nomeDoMembro']
					estadoCivil = form.cleaned_data['estadoCivil']
					sexo = form.cleaned_data['sexo']
					cargo = form.cleaned_data['cargo']
					funcaoNaIgreja = form.cleaned_data['funcaoNaIgreja']
					endereco = form.cleaned_data['endereco']
					bairro = form.cleaned_data['bairro']
					caixaPostal = form.cleaned_data['caixaPostal']
					telefone = form.cleaned_data['telefone']
					email = form.cleaned_data['email']
					dataDeNascimento = form.cleaned_data['dataDeNascimento']
					grauAcademico = form.cleaned_data['grauAcademico']
					profissao = form.cleaned_data['profissao']
					numeroDeIdentificacao = form.cleaned_data['numeroDeIdentificacao']
					conjuge = form.cleaned_data['conjuge']
					filiacaoPai = form.cleaned_data['filiacaoPai']
					filiacaoMae = form.cleaned_data['filiacaoMae']
					dataDeConversao = form.cleaned_data['dataDeConversao']
					procedencia = form.cleaned_data['procedencia']
					formaDeAdmissao = form.cleaned_data['formaDeAdmissao']
					dataDeBaptismo = form.cleaned_data['dataDeBaptismo']
					localDeBaptismo = form.cleaned_data['localDeBaptismo']
					dataDeConsagracaoDiacono = form.cleaned_data['dataDeConsagracaoDiacono']
					dataDeConsagracaoEvangelista = form.cleaned_data['dataDeConsagracaoEvangelista']
					dataDeConsagracaoPastor = form.cleaned_data['dataDeConsagracaoPastor']
					dataDeConsagracaoMissionario = form.cleaned_data['dataDeConsagracaoMissionario']
					

					new_membro=Membro(nomeDoMembro=nomeDoMembro, estadoCivil=estadoCivil, sexo=sexo,
						cargo = cargo, funcaoNaIgreja=funcaoNaIgreja, endereco=endereco, bairro=bairro, provincia=provincia, caixaPostal=caixaPostal,
						telefone=telefone, email=email, dataDeNascimento=dataDeNascimento, pais=pais, grauAcademico=grauAcademico,
						profissao=profissao, numeroDeIdentificacao=numeroDeIdentificacao, conjuge=conjuge, filiacaoPai=filiacaoPai,
						filiacaoMae=filiacaoMae, dataDeConversao=dataDeConversao, procedencia=procedencia, formaDeAdmissao= formaDeAdmissao,
						dataDeBaptismo=dataDeBaptismo, localDeBaptismo=localDeBaptismo, dataDeConsagracaoDiacono= dataDeConsagracaoDiacono,
						dataDeConsagracaoEvangelista= dataDeConsagracaoEvangelista, dataDeConsagracaoPastor=dataDeConsagracaoPastor,
						dataDeConsagracaoMissionario=dataDeConsagracaoMissionario, departamento=departamento,igreja=igreja,
						numeroDeMembro=Membro.objects.count()+1, data=date.today(), foto=request.FILES['foto'])
					
					salvar=new_membro.save()
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=membro')
				
			else:
				form = MembroForm()

			provincia = Provincia.objects.all()
			pais = Pais.objects.all()
			departamento=Departamento.objects.all()
			igreja = Igreja.objects.last()

			return render(request, 'homeMembro.html',{'form':form,'provincia':provincia,'pais':pais,'departamento':departamento,'igreja':igreja})



					

	except:
		return HttpResponseRedirect('/login')
	
#Queries 

def get_nome(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id and  nomeDoMembro like %s ",("%" + informacao +"%",));
	return dictfetchall(query)

def get_numero_membro(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id and  numeroDeMembro like %s ", ("%" + informacao + "%",));
	return dictfetchall(query)

def get_profissao_membro(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id and  profissao like %s ", ("%" + informacao + "%",));
	return dictfetchall(query)

def get_funcao_membro(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id and  funcaoNaIgreja like %s ", ("%" + informacao + "%",));
	return dictfetchall(query)

def get_grau_membro(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id and grauAcademico = '%s' " %informacao);
	return dictfetchall(query)
def get_todos(informacao):
	query=connection.cursor()
	query.execute("select DjangoOnIis_membro.id, nomeDoMembro, numeroDeMembro, estadoCivil, sexo, funcaoNaIgreja, telefone,DjangoOnIis_departamento.nomeDoDepartamento from DjangoOnIis_membro, DjangoOnIis_departamento where DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id ");
	return dictfetchall(query)

def get_editar_membro(valor):
	query = connection.cursor()
	query.execute("select DjangoOnIis_membro.nomeDoMembro,DjangoOnIis_membro.foto, DjangoOnIis_membro.dataDeNascimento,DjangoOnIis_membro.sexo, DjangoOnIis_provincia.nomeDaProvincia,DjangoOnIis_pais.nomeDoPais, DjangoOnIis_membro.estadoCivil, DjangoOnIis_membro.conjuge, DjangoOnIis_membro.filiacaoPai, DjangoOnIis_membro.filiacaoMae, DjangoOnIis_membro.numeroDeIdentificacao, DjangoOnIis_membro.endereco, DjangoOnIis_membro.bairro, DjangoOnIis_membro.telefone, DjangoOnIis_membro.email, DjangoOnIis_membro.grauAcademico, DjangoOnIis_membro.profissao, DjangoOnIis_membro.numeroDeMembro,DjangoOnIis_membro.dataDeConversao, DjangoOnIis_membro.procedencia, DjangoOnIis_membro.formaDeAdmissao, DjangoOnIis_membro.dataDeBaptismo, DjangoOnIis_membro.localDeBaptismo, DjangoOnIis_membro.dataDeConsagracaoDiacono, DjangoOnIis_membro.dataDeConsagracaoEvangelista,DjangoOnIis_membro.dataDeConsagracaoPastor, DjangoOnIis_membro.dataDeConsagracaoMissionario, DjangoOnIis_departamento.nomeDoDepartamento, DjangoOnIis_igreja.nomeDaIgreja from DjangoOnIis_membro left join DjangoOnIis_departamento ON DjangoOnIis_membro.departamento_id = DjangoOnIis_departamento.id left Join  DjangoOnIis_pais ON DjangoOnIis_membro.pais_id = DjangoOnIis_pais.id left join DjangoOnIis_provincia ON DjangoOnIis_membro.provincia_id = DjangoOnIis_provincia.id LEFT JOIN DjangoOnIis_igreja ON DjangoOnIis_membro.igreja_id= DjangoOnIis_igreja.id where DjangoOnIis_membro.id = '%s'" % valor);
	return dictfetchall(query)

def removerMembro(valor):
	query = connection.cursor()
	query.execute("delete from DjangoOnIis_membro where id = '%s'" % valor);
	return dictfetchall(query)

def pesquisarDizimo(valor, ano):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_dizimo where nomeDomembro_id = '%s' and anoDoDizimo = '%s'" %(valor, ano)) ;
	return dictfetchall(query)

def pesquisarDizimoTodos(valor):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_dizimo where nomeDomembro_id = '%s'" %valor);
	return dictfetchall(query)

def pesquisarContribuicao(valor, ano):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_contribuicao where nomeDomembro_id = '%s' and anoDaContribuicao = '%s'" %(valor, ano)) ;
	return dictfetchall(query)

def pesquisarContribuicaoTodos(valor):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_contribuicao where nomeDomembro_id = '%s'" %valor);
	return dictfetchall(query)


def totalAno(ano):
	query = connection.cursor()
	query.execute("select sum(valorDoDizimo) as totalDizimo,anoDoDizimo, mesDoDizimo, dataDoDizimo from DjangoOnIis_dizimo where  anoDoDizimo ='%s' group by mesDoDizimo order by field(mesDoDizimo, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')" %ano);
	return dictfetchall(query)

def totalOfertaAno(ano):
	query = connection.cursor()
	query.execute("select sum(valorDaOferta) as totalOferta,anoDaOferta, mesDaOferta, dataDaOferta from DjangoOnIis_oferta where  anoDaOferta ='%s' group by mesDaOferta order by field(mesDaOferta, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')" %ano);
	return dictfetchall(query)

def totalContribuicaoAno(ano):
	query = connection.cursor()
	query.execute("select sum(valorDaContribuicao) as totalContribuicao,anoDaContribuicao, mesDaContribuicao, dataDaContribuicao, descricaoDoProjeto from DjangoOnIis_contribuicao, DjangoOnIis_projeto where DjangoOnIis_projeto.id=DjangoOnIis_contribuicao.descricaoDaContribuicao_id and  anoDaContribuicao ='%s' group by descricaoDaContribuicao_id order by anoDaContribuicao" %ano);
	return dictfetchall(query)


def get_noticias_pesquisa(pesquisa):
	query = connection.cursor()
	query.execute("select id,noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where titulo like '%s' or noticia like '%s' order by dataPublicacao desc" %("%" + pesquisa + "%","%" + pesquisa + "%"));
	return dictfetchall(query)


def pesquisarMembro(request):
	try:
		if request.session['user']:
			content ={'Nao existem resultados'}
			opcao = request.GET.get('opcao')
			informacao = request.GET.get('informacao')
			resultado = Membro.objects.all()
			print resultado
			if opcao == 'Nome':
				resultado = get_nome(informacao)
				content ={'query':opcao, 'resultado':resultado}
			elif opcao == 'Numero de Membro':
				resultado = get_numero_membro(informacao)
				content = {'query':opcao, 'resultado':resultado}
			elif opcao == 'Profissao':
				resultado = get_profissao_membro(informacao)
				content = {'query':opcao, 'resultado':resultado}
			elif opcao == 'Funcao':
				resultado = get_funcao_membro(informacao)
				content = {'query':opcao, 'resultado':resultado}
			elif opcao == 'Todos':
				resultado = get_todos(informacao)
				content = {'query':opcao, 'resultado':resultado}
			else:
				resultado = get_grau_membro(informacao)
				content = {'query':opcao, 'resultado':resultado}

			template = 'pesquisarMembro.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'resultado':resultado, 'igreja':igreja})

	except:
		return HttpResponseRedirect('/login')

	

def editarMembro(request):
	try:
		if request.session['user']:
        		valor = request.GET.get('id')

        		resultado = get_editar_membro(valor)
        		print resultado
        		if request.method == 'POST':
                		form = MembroForm(request.POST, request.FILES)
                		if form.is_valid():
                        		resultado = Membro.objects.get(pk=valor)
                        		resultado.provincia = Provincia.objects.get(nomeDaProvincia=form.cleaned_data['provincia'])
                        		resultado.pais = Pais.objects.get(nomeDoPais=form.cleaned_data['pais'])
                        		resultado.departamento = Departamento.objects.get(nomeDoDepartamento=form.cleaned_data['departamento'])
                        		resultado.igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
                        		resultado.nomeDoMembro = form.cleaned_data['nomeDoMembro']
                        		resultado.estadoCivil = form.cleaned_data['estadoCivil']
                        		resultado.sexo = form.cleaned_data['sexo']
                        		resultado.cargo = form.cleaned_data['cargo']
                        		resultado.funcaoNaIgreja = form.cleaned_data['funcaoNaIgreja']
                        		resultado.endereco = form.cleaned_data['endereco']
                        		resultado.bairro = form.cleaned_data['bairro']
                        		resultado.caixaPostal = form.cleaned_data['caixaPostal']
                        		resultado.telefone = form.cleaned_data['telefone']
                        		resultado.email = form.cleaned_data['email']
                        		resultado.dataDeNascimento = form.cleaned_data['dataDeNascimento']
                        		resultado.grauAcademico = form.cleaned_data['grauAcademico']
                        		resultado.profissao = form.cleaned_data['profissao']
                        		resultado.numeroDeIdentificacao = form.cleaned_data['numeroDeIdentificacao']
                        		resultado.conjuge = form.cleaned_data['conjuge']
                        		resultado.filiacaoPai = form.cleaned_data['filiacaoPai']
                        		resultado.filiacaoMae = form.cleaned_data['filiacaoMae']
                        		resultado.dataDeConversao = form.cleaned_data['dataDeConversao']
                        		resultado.procedencia = form.cleaned_data['procedencia']
                        		resultado.formaDeAdmissao = form.cleaned_data['formaDeAdmissao']
                        		resultado.dataDeBaptismo = form.cleaned_data['dataDeBaptismo']
                        		resultado.localDeBaptismo = form.cleaned_data['localDeBaptismo']
                        		resultado.dataDeConsagracaoDiacono = form.cleaned_data['dataDeConsagracaoDiacono']
                        		resultado.dataDeConsagracaoEvangelista = form.cleaned_data['dataDeConsagracaoEvangelista']
                        		resultado.dataDeConsagracaoPastor = form.cleaned_data['dataDeConsagracaoPastor']
                        		resultado.dataDeConsagracaoMissionario = form.cleaned_data['dataDeConsagracaoMissionario']
                        		resultado.numeroDeMembro = form.cleaned_data['numeroDeMembro']
                        		resultado.foto=request.FILES['foto']
                        		resultado.save()
                        		return HttpResponseRedirect('/gestao/membro/pesquisar/')

        		else:
        		        form = MembroForm()
        		template = 'editarMembro.html'
        		provincia=Provincia.objects.all()
        		pais =Pais.objects.all()
        		departamento=Departamento.objects.all()
        		igreja=Igreja.objects.last()
        		return render (request,template,{'form':form, 'resultado':resultado,'provincia':provincia,'pais':pais,'departamento':departamento,'igreja':igreja})
					

	except:
		return HttpResponseRedirect('/login')

def eliminarMembro(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			print valor
			resultado = get_editar_membro(valor)
			print resultado
			try:
				if request.method == 'POST':
					form = MembroForm(request.POST)
					removerMembro(valor)
					return HttpResponseRedirect('/gestao/membro/pesquisar/')
				else:
					form = MembroForm()
			except:
				return HttpResponseRedirect('/gestao/erros/eliminar/')
			igreja = Igreja.objects.last()
			template = 'eliminarMembro.html'
			return render(request, template, {'form':form, 'resultado':resultado, 'igreja':igreja})					
	except:
		return HttpResponseRedirect('/login')
	





	
def visualizarMembro(request):
	try:
		if request.session['user']:

			valor = request.GET.get('id')
			print valor
			resultado = get_editar_membro(valor)
			print resultado
			
			if request.method == 'POST':
				form = MembroForm(request.POST)
				return HttpResponseRedirect('/gestao/membro/pesquisar/')
			else:
				form = MembroForm()
			template = 'visualizarMembro.html'
			provincia=Provincia.objects.all()
			pais =Pais.objects.all()
			departamento=Departamento.objects.all()
			igreja=Igreja.objects.last()
			return render (request,template,{'form':form, 'resultado':resultado,'provincia':provincia,'pais':pais,'departamento':departamento,'igreja':igreja})						

	except:
		return HttpResponseRedirect('/login')
	
def dizimo(request):
	try:
		if request.session['user']:
			if request.method =='POST':
				form = DizimoForm(request.POST)
				if form.is_valid():

					nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					valorDoDizimo = form.cleaned_data['valorDoDizimo']
					dataDoDizimo = form.cleaned_data['dataDoDizimo']
					mesDoDizimo = form.cleaned_data['mesDoDizimo']
					anoDoDizimo = form.cleaned_data['anoDoDizimo']
					#print form.cleaned_data['nome']

					new_dizimo, created = Dizimo.objects.get_or_create(nomeDoMembro=nomeDoMembro, igreja=igreja, valorDoDizimo=valorDoDizimo,dataDoDizimo=dataDoDizimo,
						mesDoDizimo=mesDoDizimo, anoDoDizimo=anoDoDizimo)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=financas/dizimos')

			else:
				form = DizimoForm()
			valor = request.GET.get('id')
			request.session['id']=valor
			if not request.session['id']:
				membro = Membro.objects.order_by('nomeDoMembro')
			else:
				membro = Membro.objects.filter(pk=request.session['id'])

			template = 'dizimo.html'
			igreja = Igreja.objects.last()
			print membro

			return render(request, template, {'form':form, 'membro':membro, 'igreja':igreja})

					

	except:
		return HttpResponseRedirect('/login')


def get_editar_dizimo(valor):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_dizimo where id='%s'" %valor)
	return dictfetchall(query)

def editarDizimo(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			request.session['id'] = valor
			resultado = get_editar_dizimo(request.session['id'])
			if request.method == 'POST':
				form = DizimoForm(request.POST)
				if form.is_valid():
					nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					valorDoDizimo = form.cleaned_data['valorDoDizimo']
					dataDoDizimo = form.cleaned_data['dataDoDizimo']
					mesDoDizimo = form.cleaned_data['mesDoDizimo']
					anoDoDizimo = form.cleaned_data['anoDoDizimo']
					

					created = Dizimo.objects.filter(pk=request.session['id']).update(nomeDoMembro=nomeDoMembro, igreja=igreja, valorDoDizimo=valorDoDizimo,dataDoDizimo=dataDoDizimo,
						mesDoDizimo=mesDoDizimo, anoDoDizimo=anoDoDizimo)
					return HttpResponseRedirect('/gestao/membro/pesquisar/')

			else:
				form = DizimoForm()
			membro = Membro.objects.filter(pk=resultado[0]['nomeDoMembro_id'])
			igreja = Igreja.objects.last()
			template = 'editarDizimo.html'
			return render(request, template, {'form':form, 'resultado':resultado, 'igreja':igreja, 'membro':membro})

							

	except:
		return HttpResponseRedirect('/login')
	

def eliminarDizimo(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			request.session['id']=valor 
			resultado = get_editar_dizimo(request.session['id'])
			try:
				if request.method == 'POST':
					resultado = Dizimo.objects.filter(pk=request.session['id']).delete()
					return HttpResponseRedirect('/gestao/financas/contribuicao/pesquisar/')

				template = 'eliminarDizimo.html'
				membro = Membro.objects.filter(pk=resultado[0]['nomeDoMembro_id'])
				igreja = Igreja.objects.last()
			except IndexError:
				return HttpResponseRedirect('/gestao/membro/pesquisar/')

			return render(request, template, {'resultado':resultado, 'membro':membro, 'igreja':igreja})
							
	except:
		return HttpResponseRedirect('/login')

	

def projeto(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = ProjetoForm(request.POST)
				if form.is_valid():
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					descricaoDoProjeto = form.cleaned_data['descricaoDoProjeto']
					orcamento = form.cleaned_data['orcamento']

					new_projeto, created = Projeto.objects.get_or_create(igreja=igreja, descricaoDoProjeto=descricaoDoProjeto, orcamento=orcamento)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=financas/projetos')

			else:
				form = ProjetoForm()

			template = 'projeto.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'form':form, 'igreja':igreja})

							

	except:
		return HttpResponseRedirect('/login')
	
def contribuicao(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = ContribuicaoForm(request.POST)
				if form.is_valid():
					nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					valorDaContribuicao = form.cleaned_data['valorDaContribuicao']
					descricaoDaContribuicao = Projeto.objects.get(descricaoDoProjeto=form.cleaned_data['descricaoDaContribuicao'])
					dataDaContribuicao = form.cleaned_data['dataDaContribuicao']
					mesDaContribuicao = form.cleaned_data['mesDaContribuicao']
					anoDaContribuicao = form.cleaned_data['anoDaContribuicao']
					new_contribuicao, created = Contribuicao.objects.get_or_create(nomeDoMembro=nomeDoMembro,igreja=igreja,valorDaContribuicao=valorDaContribuicao,descricaoDaContribuicao=descricaoDaContribuicao, dataDaContribuicao=dataDaContribuicao,
						mesDaContribuicao=mesDaContribuicao, anoDaContribuicao=anoDaContribuicao)

					return HttpResponseRedirect('/gestao/financas/contribuicao/pesquisar/')
			else:
				form = ContribuicaoForm()

			template = 'contribuicao.html'
			valor = request.GET.get('id')
			request.session['id'] = valor
			if not request.session['id']:
				membro = Membro.objects.order_by('nomeDoMembro')
			else:
				membro = Membro.objects.filter(pk=request.session['id'])
			igreja = Igreja.objects.last()
			projeto= Projeto.objects.order_by('descricaoDoProjeto')
			return render (request, template, {'form':form, 'membro':membro, 'igreja':igreja ,'projeto':projeto})

							

	except:
		return HttpResponseRedirect('/login')


	
def get_editar_contribuicao(valor):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_contribuicao where id='%s'" %valor)
	return dictfetchall(query)



def editarContribuicao(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			request.session['id'] = valor
			resultado = get_editar_contribuicao(request.session['id'])
			if request.method == 'POST':
				form = ContribuicaoForm(request.POST)
				if form.is_valid():
					nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					valorDaContribuicao = form.cleaned_data['valorDaContribuicao']
					descricaoDaContribuicao = Projeto.objects.get(descricaoDoProjeto=form.cleaned_data['descricaoDaContribuicao'])
					dataDaContribuicao = form.cleaned_data['dataDaContribuicao']
					mesDaContribuicao = form.cleaned_data['mesDaContribuicao']
					anoDaContribuicao = form.cleaned_data['anoDaContribuicao']
					created = Contribuicao.objects.filter(pk=request.session['id']).update(nomeDoMembro=nomeDoMembro,igreja=igreja,valorDaContribuicao=valorDaContribuicao,descricaoDaContribuicao=descricaoDaContribuicao, dataDaContribuicao=dataDaContribuicao,
						mesDaContribuicao=mesDaContribuicao, anoDaContribuicao=anoDaContribuicao)

					return HttpResponseRedirect('/gestao/financas/contribuicao/pesquisar/')
			else:
				form = ContribuicaoForm()
			membro = Membro.objects.filter(pk=resultado[0]['nomeDoMembro_id'])
			igreja = Igreja.objects.last()
			projeto = Projeto.objects.order_by('descricaoDoProjeto')
			template = 'editarContribuicao.html'

			return render(request, template, {'form':form, 'resultado':resultado, 'membro':membro, 'igreja':igreja, 'projeto':projeto})

					

	except:
		return HttpResponseRedirect('/login')
		
	
def eliminarContribuicao(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			request.session['id']=valor 
			resultado = get_editar_contribuicao(request.session['id'])
			try:
				if request.method == 'POST':
					resultado = Contribuicao.objects.filter(pk=request.session['id']).delete()
					return HttpResponseRedirect('/gestao/financas/contribuicao/pesquisar/')

				template = 'eliminarContribuicao.html'
				membro = Membro.objects.filter(pk=resultado[0]['nomeDoMembro_id'])
				igreja = Igreja.objects.last()
				projeto = Projeto.objects.filter(pk=resultado[0]['descricaoDaContribuicao_id'])
			except IndexError:
				return HttpResponseRedirect('/gestao/financas/contribuicao/pesquisar/')

			return render(request, template, {'resultado':resultado, 'membro':membro, 'projeto':projeto, 'igreja':igreja})

							

	except:
		return HttpResponseRedirect('/login')
	
def oferta(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = OfertaForm(request.POST)
				if form.is_valid():
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					valorDaOferta = form.cleaned_data['valorDaOferta']
					dataDaOferta =form.cleaned_data['dataDaOferta']
					mesDaOferta = form.cleaned_data['mesDaOferta']
					anoDaOferta = form.cleaned_data['anoDaOferta']

					new_oferta, created = Oferta.objects.get_or_create(igreja=igreja,valorDaOferta=valorDaOferta, dataDaOferta=dataDaOferta,
						mesDaOferta=mesDaOferta, anoDaOferta=anoDaOferta)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=financas/ofertas')
			else:
				form = ContribuicaoForm()

			template = 'oferta.html'
			igreja = Igreja.objects.last()
			return render (request, template, {'form':form, 'igreja':igreja})


							

	except:
		return HttpResponseRedirect('/login')
	
def visualizarDizimo(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			ano = request.GET.get('ano')
			if request.GET.get('id'):
				request.session['id'] = valor

			resultado = pesquisarDizimoTodos(valor)
			if ano and ano!='Todos':
				resultado=Dizimo.objects.filter(nomeDoMembro_id=request.session['id'], anoDoDizimo=ano)

			else:
				resultado = Dizimo.objects.filter(nomeDoMembro_id=request.session['id'])

			membro = Membro.objects.filter(pk=request.session['id'])
				
			template = 'visualizarDizimo.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'resultado':resultado, 'membro':membro, 'igreja':igreja})
							

	except:
		return HttpResponseRedirect('/login')
	

def totalValores(request):
	try:
		if request.session['user']:
			opcao = request.GET.get('anoescolha')
			resultado = ''
			if opcao:
				resultado = totalAno(opcao)
				print resultado
			template = 'totalValoresDizimos.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'resultado':resultado, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')
	


def funcionario(request):
	try:
		if request.session['user']:
			if request.method == 'POST':
				form = FuncionarioForm(request.POST,request.FILES)
				if form.is_valid():
					nomeDoFuncionario = form.cleaned_data['nomeDoFuncionario']
					estadoCivil = form.cleaned_data['estadoCivil']
					sexo = form.cleaned_data['sexo']
					cargo = form.cleaned_data['cargo']
					endereco = form.cleaned_data['endereco']
					bairro = form.cleaned_data['bairro']
					provincia = Provincia.objects.get(nomeDaProvincia=form.cleaned_data['provincia'])
					caixaPostal = form.cleaned_data['caixaPostal']
					telefone = form.cleaned_data['telefone']
					email = form.cleaned_data['email']
					dataDeNascimento = form.cleaned_data['dataDeNascimento']
					pais = Pais.objects.get(nomeDoPais=form.cleaned_data['pais'])
					grauAcademico = form.cleaned_data['grauAcademico']
					profissao = form.cleaned_data['profissao']
					numeroDeIdentificacao = form.cleaned_data['numeroDeIdentificacao']
					filiacaoPai = form.cleaned_data['filiacaoPai']
					filiacaoMae = form.cleaned_data['filiacaoMae']
					numeroDeFuncionario = form.cleaned_data['numeroDeFuncionario']
					salarioBase = form.cleaned_data['salarioBase']
					

					new_funcionario= Funcionario(nomeDoFuncionario=nomeDoFuncionario,estadoCivil=estadoCivil,
						sexo=sexo, cargo=cargo, endereco=endereco, bairro=bairro, provincia=provincia,caixaPostal=caixaPostal, telefone=telefone,
						email=email, dataDeNascimento=dataDeNascimento, pais=pais, grauAcademico=grauAcademico, profissao=profissao,
						numeroDeIdentificacao=numeroDeIdentificacao, filiacaoPai=filiacaoPai, filiacaoMae=filiacaoMae, numeroDeFuncionario=numeroDeFuncionario,
						salarioBase=salarioBase,foto=request.FILES['foto'])
					new_funcionario.save()
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=rh/funcionario')
			else:
				form= FuncionarioForm()
			pais = Pais.objects.order_by('nomeDoPais')
			provincia = Provincia.objects.order_by('nomeDaProvincia')
			igreja = Igreja.objects.last()
			template = 'funcionario.html'
			return render(request, template, {'form':form, 'pais':pais, 'provincia':provincia, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')
	
def get_funcionario(informacao):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_funcionario where nomeDoFuncionario='%s'" %informacao)
	return dictfetchall(query)

def get_funcionarioId(informacao):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_funcionario where numeroDeFuncionario='%s'" %informacao)
	return dictfetchall(query)

def pesquisarFuncionario(request):
	try:
		if request.session['user']:
			opcao = request.GET.get('opcao')
			informacao = request.GET.get('informacao')

			if opcao == 'Todos':
				resultado = Funcionario.objects.order_by('nomeDoFuncionario')
			elif opcao == 'Nome':
				resultado = get_funcionario(informacao)
			else:
				resultado = get_funcionarioId(informacao)

			pais = Pais.objects.order_by('pais')
			provincia = Provincia.objects.order_by('provincia')
			igreja = Igreja.objects.last()
			template = 'pesquisarFuncionario.html'
			return render(request, template, {'resultado':resultado, 'pais':pais, 'provincia':provincia, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')
	


def get_salario(funcionario, ano):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_salario where nomeDoFuncionario_id='%s' and salarioAno='%s'" %(funcionario, ano))
	return dictfetchall(query)

def get_salarioTodos(funcionario):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_salario where nomeDoFuncionario_id='%s'" %funcionario)
	return dictfetchall(query)

def get_editar_salario(valor):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_salario where id='%s'" %valor)
	return dictfetchall(query)


def visualizarSalario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			ano = request.GET.get('ano')
			print ano

			if request.GET.get('id'):
				request.session['id'] = valor
			resultado=get_salarioTodos(valor)
			if ano and ano!='Todos':
				resultado = get_salario(request.session['id'],ano)
			else:
				resultado = get_salarioTodos(request.session['id'])
			
			funcionario = Funcionario.objects.get(pk=request.session['id'])
			print funcionario.salarioBase
			template= 'visualizarSalario.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'resultado':resultado, 'funcionario':funcionario, 'igreja':igreja})

							
	except:
		return HttpResponseRedirect('/login')
	

def inserirSalario(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = SalarioForm(request.POST)
				if form.is_valid():
					nomeDoFuncionario=Funcionario.objects.get(nomeDoFuncionario=form.cleaned_data['nomeDoFuncionario'])
					salarioAno = form.cleaned_data['salarioAno']
					salarioMes= form.cleaned_data['salarioMes']
					salarioSS = form.cleaned_data['salarioSS']
					salarioIRT = form.cleaned_data['salarioIRT']
					salarioNumerodeFaltas = form.cleaned_data['salarioNumerodeFaltas']
					salarioBonus = form.cleaned_data['salarioBonus']
					salarioLiquido = form.cleaned_data['salarioLiquido']

					new_salario, created = Salario.objects.get_or_create(nomeDoFuncionario=nomeDoFuncionario, salarioAno=salarioAno,
							salarioMes=salarioMes, salarioSS=salarioSS, salarioIRT=salarioIRT, salarioNumerodeFaltas=salarioNumerodeFaltas,
							salarioBonus=salarioBonus, salarioLiquido=salarioLiquido)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=rh/funcionario/salario/inserir')

			else:
				form=SalarioForm()
			valor = request.GET.get('id')
			request.session['id'] =valor
			if not request.session['id']:
				funcionario = Funcionario.objects.order_by('nomeDoFuncionario') 
			else:
				funcionario = Funcionario.objects.filter(pk=request.session['id'])
			template = 'inserirSalario.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'form':form, 'funcionario':funcionario, 'igreja':igreja})

							
	except:
		return HttpResponseRedirect('/login')

	
def EditarSalario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = get_editar_salario(valor)
			print resultado
			if request.method == 'POST':
				form = SalarioForm(request.POST)
				if form.is_valid():
					nomeDoFuncionario=Funcionario.objects.get(nomeDoFuncionario=form.cleaned_data['nomeDoFuncionario'])
					salarioAno = form.cleaned_data['salarioAno']
					salarioMes= form.cleaned_data['salarioMes']
					salarioSS = form.cleaned_data['salarioSS']
					salarioIRT = form.cleaned_data['salarioIRT']
					salarioNumerodeFaltas = form.cleaned_data['salarioNumerodeFaltas']
					salarioBonus = form.cleaned_data['salarioBonus']
					salarioLiquido = form.cleaned_data['salarioLiquido']

					created = Salario.objects.filter(pk=valor).update(nomeDoFuncionario=nomeDoFuncionario, salarioAno=salarioAno,
							salarioMes=salarioMes, salarioSS=salarioSS, salarioIRT=salarioIRT, salarioNumerodeFaltas=salarioNumerodeFaltas,
							salarioBonus=salarioBonus, salarioLiquido=salarioLiquido)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=rh/funcionario/salario/inserir')
			else:
				form=SalarioForm()

			funcionario = Funcionario.objects.get(pk=resultado[0]['nomeDoFuncionario_id']) 
			template = 'editarSalario.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'form':form, 'funcionario':funcionario, 'resultado':resultado, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')
	

def removeSalario(valor):
	query = connection.cursor()
	query.execute("delete from DjangoOnIis_salario where id='%s'" %valor)
	return dictfetchall(query)

def eliminarSalario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = get_editar_salario(valor)
			if request.method == 'POST':
				form= SalarioForm(request.POST)
				removeSalario(valor)
				return HttpResponseRedirect('/gestao/rh/funcionario/pesquisar/')
			else:
				form=SalarioForm()

			template = 'eliminarSalarioMes.html'
			funcionario = Funcionario.objects.get(pk=resultado[0]['nomeDoFuncionario_id']) 
			igreja = Igreja.objects.last()
			return render(request, template, {'form':form, 'funcionario':funcionario, 'resultado':resultado, 'igreja':igreja})					
	except:
		return HttpResponseRedirect('/login')
	
def visualizarFuncionario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = Funcionario.objects.get(pk=valor)
			pais = Pais.objects.get(pk=resultado.pais_id)
			provincia = Provincia.objects.get(pk=resultado.provincia_id)
			template = 'visualizarFuncionario.html'
			igreja = Igreja.objects.last()

			return render (request,template,{'resultado':resultado, 'pais':pais, 'provincia':provincia, 'igreja':igreja})

							
	except:
		return HttpResponseRedirect('/login')
	

def editarFuncionario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = Funcionario.objects.get(pk=valor)
			print resultado
			if request.method == 'POST':
				form = FuncionarioForm(request.POST,request.FILES)
				if form.is_valid():
					resultado = Funcionario.objects.get(pk=valor)
					resultado.nomeDoFuncionario = form.cleaned_data['nomeDoFuncionario']
					resultado.estadoCivil = form.cleaned_data['estadoCivil']
					resultado.sexo = form.cleaned_data['sexo']
					resultado.cargo = form.cleaned_data['cargo']
					resultado.endereco = form.cleaned_data['endereco']
					resultado.bairro = form.cleaned_data['bairro']
					resultado.provincia = Provincia.objects.get(nomeDaProvincia=form.cleaned_data['provincia'])
					resultado.caixaPostal = form.cleaned_data['caixaPostal']
					resultado.telefone = form.cleaned_data['telefone']
					resultado.email = form.cleaned_data['email']
					resultado.dataDeNascimento = form.cleaned_data['dataDeNascimento']
					resultado.pais = Pais.objects.get(nomeDoPais=form.cleaned_data['pais'])
					resultado.grauAcademico = form.cleaned_data['grauAcademico']
					resultado.profissao = form.cleaned_data['profissao']
					resultado.numeroDeIdentificacao = form.cleaned_data['numeroDeIdentificacao']
					resultado.filiacaoPai = form.cleaned_data['filiacaoPai']
					resultado.filiacaoMae = form.cleaned_data['filiacaoMae']
					resultado.numeroDeFuncionario = form.cleaned_data['numeroDeFuncionario']
					resultado.salarioBase = form.cleaned_data['salarioBase']
					resultado.foto=request.FILES['foto']
					resultado.save()
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=rh/funcionario')
			else:
				form= FuncionarioForm()
			pais = Pais.objects.order_by('nomeDoPais')
			provincia = Provincia.objects.order_by('nomeDaProvincia')
			igreja = Igreja.objects.last()
			template = 'editarFuncionario.html'
			return render(request, template, {'form':form, 'pais':pais, 'provincia':provincia, 'resultado':resultado, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')

	
def eliminarFuncionario(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = Funcionario.objects.get(pk=valor)
			if request.method == 'POST':
				resultado = Funcionario.objects.filter(pk=valor).delete()
				return HttpResponseRedirect('/gestao/rh/funcionario/pesquisar/')
			
			template = 'eliminarFuncionario.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'resultado':resultado, 'igreja':igreja})
			
	except:
		return HttpResponseRedirect('/login')
	

def equipamento(request):
	try:
		if request.session['user']:
			if request.method == 'POST':
			        form = EquipamentoForm(request.POST)
			        if form.is_valid():
			            igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
		        	    nome=form.cleaned_data['nome']
		        	    marca = form.cleaned_data['marca']
		        	    numeroDeSerie = form.cleaned_data['numeroDeSerie']
		        	    dataDaAquisicao = form.cleaned_data['dataDaAquisicao']
		        	    modelo = form.cleaned_data['modelo']
		        	    localizacao = form.cleaned_data['localizacao']
		        	    estado = form.cleaned_data['estado']
		        	    preco = form.cleaned_data['preco']
		        	    obs = form.cleaned_data['obs']

		        	    new_equipamento, created=Equipamento.objects.get_or_create(igreja=igreja,nome=nome,marca=marca,numeroDeSerie=numeroDeSerie,dataDaAquisicao=dataDaAquisicao,modelo=modelo,localizacao=localizacao,estado=estado,preco=preco,obs=obs)
		        	    return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=inventario') 
			else:
				form = EquipamentoForm()
		   	template='equipamento.html'
		   	igreja = Igreja.objects.last()
		   	return render (request, template, {'form':form, 'igreja':igreja})

					
	except:
		return HttpResponseRedirect('/login')
    

def pesquisarEquipamentos(estado):
    query = connection.cursor()
    query.execute("select * from DjangoOnIis_equipamento where estado = '%s'" %estado);
    return dictfetchall(query)

def pesquisarEquipamentoTodos():
    query = connection.cursor()
    query.execute("select * from DjangoOnIis_equipamento ");
    return dictfetchall(query)

def pesquisarEquipamento(request):
	try:
		if request.session['user']:
			opcao = request.GET.get('estado')
			print opcao
		   	resultado = ''
		    	if opcao is not None and opcao != '':
		        	resultado = pesquisarEquipamentos(opcao)
		    	else:
		        	resultado=pesquisarEquipamentoTodos()
		    	igreja = Igreja.objects.last()
		    	template = 'pesquisarEquipamento.html'
		    	return render(request, template, {'resultado':resultado,'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')
    
def removerEquipamento(valor):
    query = connection.cursor()
    query.execute("delete from DjangoOnIis_equipamento where id = '%s'" % valor);
    return dictfetchall(query)

def get_editar_equipamento(valor):
    query = connection.cursor()
    query.execute("select * from DjangoOnIis_equipamento where id = '%s'" % valor);
    return dictfetchall(query)

def editarEquipamento(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
		    	resultado = get_editar_equipamento(valor)
		    	if request.method == 'POST':
		        	form = EquipamentoForm(request.POST)
		        	if form.is_valid():
		            		igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
		            		nome=form.cleaned_data['nome']
		            		marca = form.cleaned_data['marca']
		            		numeroDeSerie = form.cleaned_data['numeroDeSerie']
		            		dataDaAquisicao = form.cleaned_data['dataDaAquisicao']
		            		modelo = form.cleaned_data['modelo']
		            		localizacao = form.cleaned_data['localizacao']
		            		estado = form.cleaned_data['estado']
		            		preco = form.cleaned_data['preco']
		            		obs = form.cleaned_data['obs']

		            		created=Equipamento.objects.filter(pk=valor).update(igreja=igreja,nome=nome,marca=marca,numeroDeSerie=numeroDeSerie,dataDaAquisicao=dataDaAquisicao,modelo=modelo,localizacao=localizacao,estado=estado,preco=preco,obs=obs)
			    		return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=inventario')
			else:
		        	form = EquipamentoForm()
		    	template='editarEquipamento.html'
		    	igreja = Igreja.objects.last()
		    	return render (request, template, {'form':form, 'igreja':igreja,'resultado':resultado})

		
	except:
		return HttpResponseRedirect('/login')
    

def eliminarEquipamento(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			print valor
			resultado = get_editar_equipamento(valor)
			print resultado
		    	if request.method == 'POST':
		        	form = EquipamentoForm(request.POST)
		       		removerEquipamento(valor)
		       		return HttpResponseRedirect('/gestao/inventario/pesquisar/')
		  	else:
		       		form = MembroForm()
		   	template = 'eliminarEquipamento.html'
		    	igreja = Igreja.objects.last()
		    	return render(request, template, {'form':form, 'resultado':resultado, 'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')
    
def pesquisarProjecto(request):
	try:
		if request.session['user']:
			nome = request.GET.get('descricaoDoProjeto')
			print 'nome:', nome
			resultado = ''

			if nome=='Todos':
				resultado = Projeto.objects.order_by('descricaoDoProjeto')
			else:
				resultado = Projeto.objects.filter(descricaoDoProjeto=nome)
			template = 'pesquisarProjecto.html'
			descricaoDoProjeto = Projeto.objects.order_by('descricaoDoProjeto')
			igreja = Igreja.objects.last()

			return render(request, template, {'resultado':resultado,'igreja':igreja, 'descricaoDoProjeto':descricaoDoProjeto})

					

	except:
		return HttpResponseRedirect('/login')
	
def editarProjecto(request):

	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = Projeto.objects.get(pk=valor)
			if request.method == 'POST':
				form = ProjetoForm(request.POST)
				if form.is_valid():
					igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja'])
					descricaoDoProjeto = form.cleaned_data['descricaoDoProjeto']
					orcamento = form.cleaned_data['orcamento']

					created = Projeto.objects.filter(pk=valor).update(igreja=igreja, descricaoDoProjeto=descricaoDoProjeto, orcamento=orcamento)
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=financas/projetos')
			else:
				form = ProjetoForm()
			template = 'editarProjecto.html'
			igreja = Igreja.objects.last()
			return render(request, template,{'form':form, 'resultado':resultado, 'igreja':igreja})				

	except:
		return HttpResponseRedirect('/login')

	
def eliminarProjecto(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			resultado = Projeto.objects.get(pk=valor)
			if request.method == 'POST':
				resultado = Projeto.objects.filter(pk=valor).delete()
				return HttpResponseRedirect('/gestao/financas/projetos/pesquisar/')
			
			igreja = Igreja.objects.last()
			template = 'eliminarProjecto.html'
			return render(request, template, {'resultado':resultado, 'igreja':igreja})

					

	except:
		return HttpResponseRedirect('/login')

	

def pesquisarOferta(request):
	try:
		if request.session['user']:
			opcao = request.GET.get('anoescolha')
			resultado = ''
			if opcao:
				resultado = totalOfertaAno(opcao)
			
			igreja = Igreja.objects.last()
			template = 'pesquisarOferta.html'
			return render(request, template, {'resultado':resultado, 'igreja':igreja})
							
	except:
		return HttpResponseRedirect('/login')
	
def visualizarContribuicao(request):
	try:
		if request.session['user']:
			valor = request.GET.get('id')
			ano = request.GET.get('ano')
			if request.GET.get('id'):
				request.session['id'] = valor

			resultado = pesquisarContribuicaoTodos(valor)
			if ano and ano!='Todos':
				resultado=pesquisarContribuicao(request.session['id'],ano)
			else:
				resultado = pesquisarContribuicaoTodos(request.session['id'])

			membro = Membro.objects.filter(pk=request.session['id'])	
			igreja = Igreja.objects.last()
			template = 'visualizarContribuicao.html'
			return render(request, template, {'resultado':resultado, 'membro':membro, 'igreja':igreja})
							

	except:
		return HttpResponseRedirect('/login')


def pesquisarContribuicao(request):
	try:
		if request.session['user']:
			opcao = request.GET.get('anoescolha')
			resultado = ''
			if opcao:
				resultado = totalContribuicaoAno(opcao)
				print 'Resultado',resultado

			igreja = Igreja.objects.last()
			template = 'pesquisarContribuicao.html'
			return render(request, template, {'resultado':resultado, 'igreja':igreja})

							

	except:
		return HttpResponseRedirect('/login')
	

from .models import Noticias

def get_noticias():
	query = connection.cursor()
	query.execute("select DjangoOnIis_noticias.id,left(DjangoOnIis_noticias.noticia,100) as noticia, DjangoOnIis_noticias.titulo,DjangoOnIis_noticias.foto,DjangoOnIis_noticias.dataPublicacao,DjangoOnIis_noticias.tipo,DjangoOnIis_membro.nomeDoMembro from DjangoOnIis_noticias DjangoOnIis_noticias left join DjangoOnIis_membro on DjangoOnIis_noticias.funcionario_id=DjangoOnIis_membro.id  where DjangoOnIis_noticias.tipo like 'Normal%' or DjangoOnIis_noticias.tipo like 'Destaque%' or  DjangoOnIis_noticias.tipo like 'Evangelismo e Missoes%' or DjangoOnIis_noticias.tipo  like 'Musica%' order by DjangoOnIis_noticias.dataPublicacao desc");
	return dictfetchall(query)


def get_noticias_unica(idd):
	query = connection.cursor()
	query.execute("select id,noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where id = '%s'" % idd);
	return dictfetchall(query)

def get_comentarios(idd):
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_comentarios where noticia_id = '%s' order by id desc" % idd);
	return dictfetchall(query)

def noticias(request):
	resultado=get_noticias()
	form = NoticiasForm()
	resultado2 = Noticias.objects.all()

	template = 'noticias.html'
	return render(request,template,{'form':form,'resultado':resultado})


def publicarNoticia(request):
	if request.method== 'POST':
		form=NoticiasForm(request.POST, request.FILES)
		if form.is_valid():
				
			
			new_foto = Noticias(foto=request.FILES['foto'],titulo = form.cleaned_data['titulo'],noticia=form.cleaned_data['noticia'],
				funcionario=Membro.objects.get(nomeDoMembro=form.cleaned_data['funcionario']),dataPublicacao = datetime.date.today(),tipo=form.cleaned_data['tipo'])
			foto = new_foto.save()
			return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=noticias/publicar')

			#new_publicarNoticia, created=Noticias.objects.get_or_create(titulo=titulo,noticia=noticia,foto=foto)
	else:
		form=NoticiasForm()
	template='inserirNoticia.html'
	membro= Membro.objects.get(pk=request.session['id_user'])
	noticias=Noticias.objects.all()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'membro':membro,'noticia':noticias, 'igreja':igreja})



#CONFIGURAÇÕES

from .forms import ConfiguracoesForm
from datetime import date

def configuracoes(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = ConfiguracoesForm(request.POST,request.FILES)
				if form.is_valid():

					try:
						new_configuracoes=Configuracoes(igreja = Igreja.objects.get(nomeDaIgreja=form.cleaned_data['igreja']),imagem1=request.FILES['imagem1'],imagem2=request.FILES['imagem2'],texto1=form.cleaned_data['texto1'],
						texto2=form.cleaned_data['texto2'],texto3=form.cleaned_data['texto3'],texto4=form.cleaned_data['texto4'],texto5=form.cleaned_data['texto5']
						,texto6=form.cleaned_data['texto6'],desenvolvedores=form.cleaned_data['desenvolvedores'])
						imagem=new_configuracoes.save()
						return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=configuracoes')
					except:
						imagem1=''
						imagem2=''
						

			else:
				form=ConfiguracoesForm()
			template='configuracoes.html'
			igreja = Igreja.objects.last()
			return render(request,template,{'form':form,'igreja':igreja})
		
	except:
		return HttpResponseRedirect('/login')





#--------------------------------------------------Modulo Gestao de noticias---------------------------------------------------
def indexNoticias(request):
	resultado=get_noticias()
	form = NoticiasForm()
	resultado = get_noticias()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	template = 'indexNoticias.html'
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})


def get_noticiasTres():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias order by dataPublicacao desc limit 4");
	return dictfetchall(query)


def lerNoticias(request):
	#print request.GET.get('id')
	if request.method=='POST':
		form = ComentariosForm(request.POST)
		if form.is_valid():
			print Membro.objects.get(nomeDoMembro=form.cleaned_data['autor'])
			print Noticias.objects.get(titulo=form.cleaned_data['noticia'])



			new_lerNoticias =Comentarios(autor = Membro.objects.get(nomeDoMembro=form.cleaned_data['autor']),noticia=Noticias.objects.get(titulo=form.cleaned_data['noticia'])
				,comentario=form.cleaned_data['comentario'],data=date.today())

			new_lerNoticias.save()
	else:
		form = ComentariosForm()

	idd = request.GET.get('id')
	destaques=get_noticias_destaque()
	resultado = get_noticias_unica(idd)
	comentarios = get_comentarios(idd)
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	membro= Membro.objects.order_by('nomeDoMembro')
	template = 'lerNoticias.html'

	return render(request,template,{'igreja':igreja, 'idd':idd,'form':form,'resultado':resultado,'configuracoes':configuracoes,'membro':membro,'destaques':destaques})


def sobre(request):
	
	igreja = Igreja.objects.last()
	configuracoes = Configuracoes.objects.last()
	template = 'sobre.html'
	return render(request, template, {'igreja':igreja, 'configuracoes':configuracoes})

#HOME
def get_devocional():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Devocional' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_videos():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Videos' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_musica():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Musica' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_missoes():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Evangelismo e Missoe' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_opiniao():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Opiniao' order by dataPublicacao desc limit 3");
	return dictfetchall(query)



def get_eventos():
	query = connection.cursor()
	query.execute("select id,left(noticia,100) as noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo='Evento' order by dataPublicacao desc limit 3");
	return dictfetchall(query)
def get_noticias_destaque():
	query = connection.cursor()
	query.execute("select id,noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo = 'Destaque' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_noticias_normal():
	query = connection.cursor()
	query.execute("select id,noticia, titulo,foto,dataPublicacao,tipo from DjangoOnIis_noticias where tipo = 'Normal' order by dataPublicacao desc limit 3");
	return dictfetchall(query)

def get_programa():
	query = connection.cursor()
	query.execute("select * from DjangoOnIis_programa order by field(diaDaSemana, 'Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira','Sábado','Domingo')");
	return dictfetchall(query)


def home_site(request):
	try:
		del request.session['user']
	except Exception, e:
		a=1
	if request.method == 'POST':
		form = PesquisarHome_site(request.POST)
		if form.is_valid():

			pesquisa = form.cleaned_data['pesquisa']
			resultado= get_noticias_pesquisa(pesquisa)
			configuracoes = Configuracoes.objects.last()
			igreja = Igreja.objects.last()
			template = 'indexNoticias.html'
			return render(request,template,{'resultado':resultado,'configuracoes':configuracoes, 'igreja':igreja})
	else:

		template='home_site.html'	
		noticias_destaques=get_noticias_destaque()
		noticia1 = ''
		noticia2 = ''
		noticia3 = ''
		try:
			for i in range(len(noticias_destaques)):
				if i==0:
					noticia1=noticias_destaques[i]
				elif i==1:
					noticia2=noticias_destaques[i]
				
				else:
					noticia3=noticias_destaques[i]
		except IndexError:
			noticia1=''
			noticia2=''
			noticia3=''

		devocional=get_devocional()
		ultimo_devocional=Noticias.objects.filter(tipo='Devocional').last()
		programa= get_programa()
	
		eventos=get_eventos() #Noticias.objects.filter(tipo='Evento')
		noticiasNormais=get_noticias_normal()
		musica = get_musica()
		missoes = get_missoes()
		opiniao = get_opiniao()
		videos = get_videos()
		ano = datetime.date.today().year
		igreja= Igreja.objects.last()
		configuracoes = Configuracoes.objects.last()
		return render(request,template,{'igreja':igreja,'configuracoes':configuracoes,'noticias_destaques':noticias_destaques, 'noticia1':noticia1,'noticia2':noticia2, 'noticia3':noticia3,'noticiasNormais':noticiasNormais,'eventos':eventos,'devocional':devocional,'ultimo_devocional':ultimo_devocional,'programa':programa, 'musica':musica, 'videos':videos, 'missoes':missoes, 'opiniao':opiniao})


def homeUm(request):
	template='homeUm.html'
	noticias_destaques=get_noticias_destaque()
	noticia1=noticias_destaques[0]
	noticia2=noticias_destaques[1]
	noticia3=noticias_destaques[2]
	devocional=Noticias.objects.filter(tipo='Devocional').order_by('-id')
	ultimo_devocional=Noticias.objects.filter(tipo='Devocional').last()

	eventos=get_eventos() #Noticias.objects.filter(tipo='Evento')
	noticiasNormais=get_noticias_normal()
	configuracoes = Configuracoes.objects.last()


	return render(request,template,{'configuracoes':configuracoes,'noticias_destaques':noticias_destaques, 'noticia1':noticia1,'noticia2':noticia2, 'noticia3':noticia3,'noticiasNormais':noticiasNormais,'eventos':eventos,'devocional':devocional,'ultimo_devocional':ultimo_devocional})

def pesquisarNoticia(request):
	
	tipo=request.GET.get('tipo')
	if tipo:
		resultado=Noticias.objects.filter(tipo=tipo).order_by('-dataPublicacao')
	if tipo==None or tipo=='Todos':
		resultado=Noticias.objects.all().order_by('-dataPublicacao')
	template='pesquisarNoticia.html'
	igreja = Igreja.objects.last()
	return render(request,template,{'resultado':resultado,'tipo':tipo, 'igreja':igreja})




def EditarNotica(request):
	try:
		if request.session['user']:
			idd = request.GET.get('id')
			resultado = Noticias.objects.get(pk=idd)
			print '-----------',resultado.noticia
			if request.method== 'POST':
				form=NoticiasForm(request.POST, request.FILES)
				if form.is_valid():
					print 'olaaaaa'			
					resultado = Noticias.objects.get(pk=idd)
					resultado.foto=request.FILES['foto']
					resultado.titulo = form.cleaned_data['titulo']
					resultado.noticia=form.cleaned_data['noticia']
					resultado.funcionario=Membro.objects.get(nomeDoMembro=form.cleaned_data['funcionario'])
					resultado.dataPublicacao = date.today()
					resultado.tipo=form.cleaned_data['tipo']
					resultado.save()
					return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=noticias/publicar')

					#new_publicarNoticia, created=Noticias.objects.get_or_create(titulo=titulo,noticia=noticia,foto=foto)
			else:
				form=NoticiasForm()
			template='editarNoticia.html'
			membro= Membro.objects.order_by('nomeDoMembro')
			noticias=Noticias.objects.all()
			igreja = Igreja.objects.last()
			return render(request,template,{'form':form,'membro':membro,'noticia':noticias,'resultado':resultado, 'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')
	

def removerNoticia(valor):
	query = connection.cursor()
	query.execute("delete from DjangoOnIis_noticias where id = '%s'" % valor);
	return dictfetchall(query)


def eliminarNotica(request):
	try:
		if request.session['user']:
			idd = request.GET.get('id')
			print idd
			resultado = Noticias.objects.get(pk=idd)
			print resultado
			
			if request.method == 'POST':
				form = NoticiasForm(request.POST)
				removerNoticia(idd)
				return HttpResponseRedirect('/gestao/noticias/pesquisar/')
			else:
				form = NoticiasForm()
			template = 'eliminarNoticia.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'form':form, 'resultado':resultado, 'igreja':igreja})

				
	except:
		return HttpResponseRedirect('/login')
	

def programa(request):
	try:
		if request.session['user']:
			if request.method=='POST':
				form = ProgramaForm(request.POST)
				if form.is_valid():


					new_configuracoes=Programa(diaDaSemana =form.cleaned_data['diaDaSemana'],descricao=form.cleaned_data['descricao'])
					new_configuracoes.save()
					return HttpResponseRedirect('/gestao/')
					
			else:
				form=ProgramaForm()
			
			igreja = Igreja.objects.last()
			template='inserirPrograma.html'
			return render(request,template,{'form':form, 'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')

	


#____________________________________________________________Login____________________________________________________________
"""def login(request):
	email = request.GET.get('email')
	password = request.GET.get('password')
	content =''
	if request.method =='GET':
		try:
			resultado = User.objects.filter(userEmail=email, userPassword=password)
			if resultado:
				return HttpResponseRedirect('/gestao/')
			else:
				content='Username e Password inválida'
		except IndexError:
				return HttpResponse('Log out')
	
	
	
	template = 'login.html'
	
	return render(request, template, {'content':content})


def pesquisarUser(email,password):
    query = connection.cursor()
    query.execute("select * from DjangoOnIis_user where userEmail = '' and userPassword=''" %(email, password));
    return dictfetchall(query) """



#________________________________________________________REPORT______________________________________________________________



def cartaDeRecomendacao1(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    other = Membro.objects.last()
    nome = other.nomeDoMembro
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="carta de recomendacao.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = letter
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setLineWidth(.3)
    p.drawCentredString(300,800,"Carta de Recomendação")
    #p.line(480,747,580,747)
    p.setFont('Helvetica', 12)
    p.drawString(60, 750,'Eu José Bernardo Luacute, Pastor da Igreja, certifico que '+nome+',')
    p.drawString(30, 735,'É membro dessa igreja com o numero de membro '+other.numeroDeMembro+' passado aos '+str(other.dataDeBaptismo)+'.')
    


    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response




from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER


def myFirstPage(canvas, doc):
	Title1 = Igreja.objects.last()
	Title2 = "Carta de Recomendação de Membro"
	pageinfo = "Carta de Recomendação"
	canvas.saveState()
	canvas.setFont('Times-Bold',15)
	canvas.drawCentredString(300, 730, Title1.nomeDaIgreja)
	canvas.setFont('Times-Bold',12)
	canvas.drawCentredString(300, 705, Title2)
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"Primeira  Página / %s" % pageinfo)
	canvas.restoreState()
    
def myLaterPages(canvas, doc):
	pageinfo = "Carta de Recomendacao"
	canvas.saveState()
	canvas.setFont('Times-Roman', 9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s" % (doc.page, pageinfo))
	canvas.restoreState()



def cartaDeRecomendacao(request):
	try:
		valor = request.GET.get('numeroDeMembro')
		dados = Membro.objects.get(numeroDeMembro=valor)
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	PAGE_HEIGHT=defaultPageSize[1]
	PAGE_WIDTH=defaultPageSize[0]
	styles = getSampleStyleSheet()
	Title = "Carta de Recomendação"
	pageinfo = "Carta de Recomendacao"   
	doc = SimpleDocTemplate(response)
	Story = [Spacer(1,2*inch)]#Nao sei
	style = styles["Normal"]
	style.alignment = TA_JUSTIFY
	texto0= ("É com bastante satisfação que a %s, vem através desta informar-lhe da situação ativa e regular, dentro dos principios bíblicos e doutrinários da %s, o membro %s, podendo assim, atuar na obra de cristo nesta estimada igreja."%(dados.igreja, dados.igreja, dados.nomeDoMembro))
	texto1 = ("Eu José Bernardo Luacuti, Pastor da igreja, certifico que %s, %s, natural de %s, residente no bairro %s, filho de %s e de %s é membro em plena comunhão nessa igreja (%s) desde %s, com o número de membro: %s. Passo assim a presente carta de recomendacao que será por mim assinada e autenticada com a assinatura digital desta organizaçãodhfgsJDFGLhsdgfljhsgdFLJHgdslfhjgsLDFHGLSDJFHGALSDF kdsjfçfhd fjkDFHÇkdjsfhkjdfhçkdjhfçksdjfhçadkjhçakjfhçkdjfhçadskfjhaçsdkfjhasçdfkjhasçdkfjhaçdsfkjahsdf asdhçfkajsdhfçkajsdfhç asdfjhaçdkfj adhfça dsjhça sdjkfha çdjfh adjfhaç sdjfhça djfha çdfjkhads çfjhadsç fjahd çfjhad fjhadf jahdf çajdshf çadjhf ahdf adjsh." %(dados.nomeDoMembro, dados.estadoCivil, dados.provincia, dados.bairro, dados.filiacaoPai, dados.filiacaoMae, dados.igreja, dados.dataDeBaptismo, dados.numeroDeMembro))
	texto2 = ("Lubango, %s" %(datetime.date.today()))
	texto3 = ("O Pastor da Igreja ")
	texto4 = ("Desde ja agradecemos, Deus o abencoe!")
	
	
	p = Paragraph(texto0, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	
	p = Paragraph(texto4, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	
	p = Paragraph(texto2, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	
	p = Paragraph(texto3, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	return response


def pesquisarDocumento(request):
	informacao = request.GET.get('informacao')
	opcao = request.GET.get('opcao')
	print 'informacao', informacao
	print 'opcao', opcao
	resultado = ''
	try:
		if opcao =='Numero de Membro':
			resultado = Membro.objects.get(numeroDeMembro=informacao)
		elif opcao =='Nome':
			resultado = Membro.objects.get(nomeDoMembro=informacao)
		else:
			print ''
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')

	template='pesquisarDocumento.html'
	 

	return render(request, template, {'resultado':resultado})




from reportlab.platypus.doctemplate import SimpleDocTemplate, Image
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import styles
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



def memboPdf(request):
	try:
		ano = request.GET.get('salarioAno')
		mes = request.GET.get('salarioMes')
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')

	response = HttpResponse(content_type='application/pdf')
	doc = SimpleDocTemplate(response)
   	Catalog = []
   	styles = getSampleStyleSheet()
   	style = styles['Heading1']
   	style.alignment = TA_CENTER
   	header = Paragraph("Folha de Salario", style)

   	Catalog.append(header)
   	style = styles['Normal']
   	headings = ('Nome do Funcionario', 'Mês','SS', 'IRT','Faltas','Bonus','Salario Liquido', 'Assinatura')
   	
   	funcionario = [(p.nomeDoFuncionario, p.salarioMes, p.salarioSS, p.salarioIRT, p.salarioNumerodeFaltas, p.salarioBonus, p.salarioLiquido) for p in Salario.objects.filter(salarioAno=ano,salarioMes=mes)]
   	t = Table([headings] + funcionario)
   	t.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
   	Catalog.append(t) 
   	Catalog.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	p = Paragraph("%s" %datetime.date.today(), style)
   	Catalog.append(p)
   	objeto= Configuracoes.objects.get(pk=1)
   	p= Image(objeto.imagem1, width=100, height=50)
   	Catalog.append(p)
   	
   	doc.build(Catalog)
	"""Catalog = []
	styles = getSampleStyleSheet()
	header = Paragraph("Lista de membros", styles['Heading1'])
	Catalog.append(header)
	style = styles['Normal']
	for membro in Membro.objects.all():
		for membro in Membro.objects.all():
			p = Paragraph("%s" % membro.nomeDoMembro, style)
			Catalog.append(p)
			s = Spacer(1, 0.1*inch)
			Catalog.append(s)
	doc.build(Catalog)"""
	return response




def cartaDeRecomendacao1(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    other = Membro.objects.last()
    nome = other.nomeDoMembro
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="carta de recomendacao.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = letter
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setLineWidth(.3)
    p.drawCentredString(300,800,"Carta de Recomendação")
    #p.line(480,747,580,747)
    p.setFont('Helvetica', 12)
    p.drawString(60, 750,'Eu José Bernardo Luacute, Pastor da Igreja, certifico que '+nome+',')
    p.drawString(30, 735,'É membro dessa igreja com o numero de membro '+other.numeroDeMembro+' passado aos '+str(other.dataDeBaptismo)+'.')
    


    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response



def myFirstPage(canvas, doc):
	Title1 = Igreja.objects.last()
	Title2 = "Carta de Recomendação de Membro"
	pageinfo = "Carta de Recomendação"
	canvas.saveState()
	canvas.setFont('Times-Bold',15)
	canvas.drawCentredString(300, 730, Title1.nomeDaIgreja)
	canvas.setFont('Times-Bold',12)
	canvas.drawCentredString(300, 705, Title2)
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"Primeira  Página / %s" % pageinfo)
	canvas.restoreState()
    
def myLaterPages(canvas, doc):
	pageinfo = "Carta de Recomendacao"
	canvas.saveState()
	canvas.setFont('Times-Roman', 9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s" % (doc.page, pageinfo))
	canvas.restoreState()



def cartaDeRecomendacao(request):
	try:
		valor = request.GET.get('numeroDeMembro')
		dados = Membro.objects.get(numeroDeMembro=valor)
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	PAGE_HEIGHT=defaultPageSize[1]
	PAGE_WIDTH=defaultPageSize[0]
	styles = getSampleStyleSheet()
	Title = "Carta de Recomendação"
	pageinfo = "Carta de Recomendacao"   
	doc = SimpleDocTemplate(response)
	Story = [Spacer(1,2*inch)]#
	style = styles["Normal"]
	style.alignment = TA_JUSTIFY
	texto0= ("É com bastante satisfação que a %s, vem através desta informar-lhe da situação ativa e regular, dentro dos principios bíblicos e doutrinários da %s, o membro %s, podendo assim, atuar na obra de cristo nesta estimada igreja."%(dados.igreja, dados.igreja, dados.nomeDoMembro))
	texto1 = ("Eu José Bernardo Luacuti, Pastor da igreja, certifico que %s, %s, natural de %s, residente no bairro %s, filho de %s e de %s é membro em plena comunhão nessa igreja (%s) desde %s, com o número de membro: %s. Passo assim a presente carta de recomendacao que será por mim assinada e autenticada com a assinatura digital desta organizaçãodhfgsJDFGLhsdgfljhsgdFLJHgdslfhjgsLDFHGLSDJFHGALSDF kdsjfçfhd fjkDFHÇkdjsfhkjdfhçkdjhfçksdjfhçadkjhçakjfhçkdjfhçadskfjhaçsdkfjhasçdfkjhasçdkfjhaçdsfkjahsdf asdhçfkajsdhfçkajsdfhç asdfjhaçdkfj adhfça dsjhça sdjkfha çdjfh adjfhaç sdjfhça djfha çdfjkhads çfjhadsç fjahd çfjhad fjhadf jahdf çajdshf çadjhf ahdf adjsh." %(dados.nomeDoMembro, dados.estadoCivil, dados.provincia, dados.bairro, dados.filiacaoPai, dados.filiacaoMae, dados.igreja, dados.dataDeBaptismo, dados.numeroDeMembro))
	texto2 = ("Lubango, %s" %(datetime.date.today()))
	texto3 = ("O Pastor da Igreja ")
	texto4 = ("Desde ja agradecemos, Deus o abencoe!")
	
	p = Paragraph(texto0, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	p = Paragraph(texto4, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	p = Paragraph(texto2, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))
	
	p = Paragraph(texto3, style)
	Story.append(p)
	Story.append(Spacer(1,0.2*inch))

	doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
	return response


def configuracaoPagina(canvas, doc):
	igreja = Igreja.objects.last()
	subtitulo = "Ficha de Membro"
	pageinfo = "ficha de membro"
	canvas.saveState()
	canvas.setFont('Times-Bold',15)
	canvas.drawCentredString(300, 730, igreja.nomeDaIgreja)
	canvas.setFont('Times-Bold',12)
	canvas.drawCentredString(300, 705, subtitulo)
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s / %s" % (doc.page, pageinfo, igreja.nomeDaIgreja))
	canvas.restoreState()

from reportlab.lib.units import inch
def fichaDeMembro(request):

	valor = request.GET.get('numeroDeMembro')
	
	try:
		resultado = Membro.objects.get(numeroDeMembro=valor)
		igreja = resultado.igreja
		print igreja
	except Exception, e:
		return HttpResponseRedirect('/gestao/erros/documento/')

	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = [Spacer(1,1*inch)]
	style = styles["Heading2"]
	style.aligment= TA_LEFT
	dados = Image(resultado.foto, width=100, height=70)
	dados.hAlign ='RIGHT' 
	lista.append(dados)
	dados = Paragraph("Membro nº: %s" %resultado.numeroDeMembro, style)
	lista.append(dados)
	style = styles['Heading4']
	dados = Paragraph('Nome do Membro: %s' %resultado.nomeDoMembro, style)
	lista.append(dados)
	style = styles['Normal']
	dados = Paragraph('Estado Civil: %s  <>	Sexo: %s <>	Data de Nascimento: %s <> País: %s <> Província: %s <> Numero do Bilhete de Identidade: %s.' %(resultado.estadoCivil, resultado.sexo, resultado.dataDeNascimento, resultado.pais, resultado.provincia, resultado.numeroDeIdentificacao),style)
	lista.append(dados)
	dados = Paragraph('Nome do Pai: %s <> Nome da Mãe: <> %s Endereço: %s <> Telefone: %s <> Email: %s <> Grau Académico: %s. Profissão: %s <> Departamento: %s. '%(resultado.filiacaoPai, resultado.filiacaoMae, resultado.endereco, resultado.telefone, resultado.email, resultado.grauAcademico, resultado.profissao, resultado.departamento), style)
	lista.append(dados)
	lista.append(Spacer(1,0.3*inch))
	dados = Paragraph('%s' %datetime.date.today(), style)
	lista.append(dados)
	lista.append(Spacer(1,0.3*inch))

	#style = styles['Normal']
	#style.alignment = TA_CENTER
	dados = Paragraph('O Pastor da Igreja', style)
	lista.append(dados)
	documento.build(lista, onFirstPage=configuracaoPagina)
	
	return response

def configuracoesDaPaginaDizimo(canvas, doc):
	igreja = Igreja.objects.last()
	pageinfo = "dizimos, %s" %datetime.date.today().year
	canvas.saveState()
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s / %s" % (doc.page, pageinfo, igreja.nomeDaIgreja))
	canvas.restoreState()

def configuracoesDaPaginaContribuicao(canvas, doc):
	igreja = Igreja.objects.last()
	pageinfo = "contribuições, %s" %datetime.date.today().year
	canvas.saveState()
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s / %s" % (doc.page, pageinfo, igreja.nomeDaIgreja))
	canvas.restoreState()

def configuracoesDaPaginaOferta(canvas, doc):
	igreja = Igreja.objects.last()
	pageinfo = "Ofertas, %s" %datetime.date.today().year
	canvas.saveState()
	canvas.setFont('Times-Roman',9)
	canvas.drawString(inch, 0.75 * inch,"%d  Página / %s / %s" % (doc.page, pageinfo, igreja.nomeDaIgreja))
	canvas.restoreState()


def dizimoAnoDocumento(request):
	try:
		valor = request.GET.get('numeroDeMembro')
		pk = request.GET.get('id')
		ano = request.GET.get('ano')
		resultado = Membro.objects.get(pk=pk, numeroDeMembro=valor)
	except Exception, e:
		HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = []
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph(str(resultado.igreja), style)
	lista.append(dados)

	style = styles['Heading4']
	style.alignment = TA_CENTER
	dados = Paragraph('Dizimos do Membro no ano %s '%ano, style)
	lista.append(dados)

	style = styles['Normal']
	dados = Paragraph('Nome do Membro: %s'%resultado.nomeDoMembro, style)
	lista.append(dados)

	lista.append(Spacer(1,0.6*inch))
	style = styles['Normal']
	headings = ('Código de Pagamento', 'Data de Pagamento', 'Mês do Dízimo', 'Valor')
	dizimo = [(f.id, f.dataDoDizimo, f.mesDoDizimo, f.valorDoDizimo) for f in Dizimo.objects.filter(nomeDoMembro_id=pk, anoDoDizimo=ano)]#.order_by('dataDoDizimo')]
	tabela = Table([headings] + dizimo)
	tabela.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
	lista.append(tabela)
	lista.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	dados = Paragraph("%s" %datetime.date.today(), style)
   	lista.append(dados)
   	lista.append(Spacer(1,0.1*inch))
   	dados = Paragraph('O Tesoureiro', style)
	lista.append(dados)
	documento.build(lista, onFirstPage=configuracoesDaPaginaDizimo)

	return response



def contribuicaoAnoDocumento(request):
	try:
		valor = request.GET.get('numeroDeMembro')
		pk = request.GET.get('id')
		ano = request.GET.get('ano')
		resultado = Membro.objects.get(pk=pk, numeroDeMembro=valor)
	except Exception, e:
		HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = []
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph(str(resultado.igreja), style)
	lista.append(dados)

	style = styles['Heading4']
	style.alignment = TA_CENTER
	dados = Paragraph('Contribuições do Membro no ano %s '%ano, style)
	lista.append(dados)

	style = styles['Normal']
	dados = Paragraph('Nome do Membro: %s'%resultado.nomeDoMembro, style)
	lista.append(dados)

	lista.append(Spacer(1,0.6*inch))
	style = styles['Normal']
	headings = ('Código da Contribuição', 'Data da Contribuição', 'Mês da Contribuição', 'Código do Projeto','Valor')
	contribuicao = [(f.id, f.dataDaContribuicao, f.mesDaContribuicao, f.descricaoDaContribuicao_id, f.valorDaContribuicao) for f in Contribuicao.objects.filter(nomeDoMembro_id=pk, anoDaContribuicao=ano)]#datetime.date.today().year).order_by('dataDaContribuicao')]
	tabela = Table([headings] + contribuicao)
	tabela.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
	lista.append(tabela)
	lista.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	dados = Paragraph("%s" %datetime.date.today(), style)
   	lista.append(dados)
   	lista.append(Spacer(1,0.1*inch))
   	dados = Paragraph('O Tesoureiro', style)
	lista.append(dados)
	documento.build(lista, onFirstPage=configuracoesDaPaginaContribuicao)

	return response

def getTotalOferta(ano):
	query = connection.cursor()
	query.execute("select sum(valorDaOferta) as Total,  dataDaOferta, mesDaOferta  from DjangoOnIis_oferta where anoDaOferta='%s' group by mesDaOferta order by field(mesDaOferta, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')"%ano)
	return dictfetchall(query)

def getTotalDizimo(ano):
	query = connection.cursor()
	query.execute("select sum(valorDoDizimo) as Total,  dataDoDizimo, mesDoDizimo  from DjangoOnIis_dizimo where anoDoDizimo='%s' group by mesDoDizimo order by field(mesDoDizimo, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')"%ano)
	return dictfetchall(query)

def getTotalContribuicao(ano):
	query = connection.cursor()
	query.execute("select sum(valorDaContribuicao) as Total,  dataDaContribuicao, mesDaContribuicao  from DjangoOnIis_contribuicao where anoDaContribuicao='%s' group by mesDaContribuicao order by field(mesDaContribuicao, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')"%ano)
	return dictfetchall(query)

#_______________________________________________________Reports da gestão Finaceira(Totais Anuais)_______________________________

from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color, blue, red, grey, green, purple
from reportlab.graphics.charts.legends import Legend, TotalAnnotator
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
#from standard_colors import pdf_chart_colors, setItems
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.barcharts import VerticalBarChart

def OfertaAnoDocumento(request):
	try:
		ano = request.GET.get('ano')
		resultado = Igreja.objects.last()
		
	except Exception, e:
		HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = []
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph(str(resultado.nomeDaIgreja), style)
	lista.append(dados)

	style = styles['Heading4']
	style.alignment = TA_CENTER
	dados = Paragraph('Total de Ofertas no ano %s '%datetime.date.today().year, style)
	lista.append(dados)
	print getTotalOferta(ano)
	print len (getTotalOferta(ano))

	lista.append(Spacer(1,0.6*inch))
	style = styles['Normal']
	headings = ('Data da Oferta', 'Mês da Oferta','Total do Mês')
	f = getTotalOferta(ano)
	
	contribuicao = [(f[i]['dataDaOferta'], f[i]['mesDaOferta'], f[i]['Total']) for i in range(len(f))]
	tabela = Table([headings] + contribuicao)
	tabela.setStyle(TableStyle(
                      [('GRID', (0,0), (12,12), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
	lista.append(tabela)
	lista.append(Spacer(1,0.2*inch))
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph('Gráfico', style)
	lista.append(dados)
	dic = [(f[i]['Total']) for i in range(len(f))]
	valores = [(dic)]
	meses = [(f[i]['mesDaOferta']) for i in range(len(f))]
	d = Drawing(100, 100)
   	cht = VerticalBarChart()
   	cht.x = 90
   	cht. y = -20
   	cht.height = 125
   	cht.width = 300
   	cht.data = valores
   	cht.bars[0].fillColor = purple
   	cht.strokeColor = colors.black
   	cht.valueAxis.valueMin = 0
   	#cht.valueAxis.valueMax = 50
   	#cht.valueAxis.valueStep = 10
   	cht.categoryAxis.labels.boxAnchor = 'ne'
   	cht.categoryAxis.labels.dx = 8
   	cht.categoryAxis.labels.dy = -2
   	cht.categoryAxis.labels.angle = 30
   
   	cht.categoryAxis.categoryNames = meses
   	d.add(cht)
   	lista.append(d)
   	lista.append(Spacer(1,1.1*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	dados = Paragraph("%s" %datetime.date.today(), style)
   	lista.append(dados)
   	lista.append(Spacer(1,0.1*inch))
   	dados = Paragraph('O Tesoureiro', style)
	lista.append(dados)
   
	documento.build(lista, onFirstPage=configuracoesDaPaginaOferta)

	return response


def DizimoAnoDocumentoTotal(request):
	try:
		ano = request.GET.get('ano')
		resultado = Igreja.objects.last()
		
	except Exception, e:
		HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = []
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph(str(resultado.nomeDaIgreja), style)
	lista.append(dados)

	style = styles['Heading4']
	style.alignment = TA_CENTER
	dados = Paragraph('Total de Dízimos no ano %s '%ano, style)
	lista.append(dados)
	print getTotalOferta(ano)
	print len (getTotalOferta(ano))

	lista.append(Spacer(1,0.6*inch))
	style = styles['Normal']
	headings = ('Data do Dízimo', 'Mês do Dízimo','Total do Dízimo')
	f = getTotalDizimo(ano)
	
	contribuicao = [(f[i]['dataDoDizimo'], f[i]['mesDoDizimo'], f[i]['Total']) for i in range(len(f))]
	tabela = Table([headings] + contribuicao)
	tabela.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
	lista.append(tabela)
	lista.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	dados = Paragraph("%s" %datetime.date.today(), style)
   	lista.append(dados)
   	lista.append(Spacer(1,0.1*inch))
   	dados = Paragraph('O Tesoureiro', style)
	lista.append(dados)
	documento.build(lista, onFirstPage=configuracoesDaPaginaDizimo)

	return response

def ContribuicaoAnoDocumentoTotal(request):
	try:
		ano = request.GET.get('ano')
		resultado = Igreja.objects.last()
		
	except Exception, e:
		HttpResponseRedirect('/gestao/erros/documento/')
	response = HttpResponse(content_type='application/pdf')
	styles = getSampleStyleSheet()
	documento = SimpleDocTemplate(response)
	lista = []
	style = styles['Heading2']
	style.alignment = TA_CENTER
	dados = Paragraph(str(resultado.nomeDaIgreja), style)
	lista.append(dados)

	style = styles['Heading4']
	style.alignment = TA_CENTER
	dados = Paragraph('Total de Contribuições no ano %s '%ano, style)
	lista.append(dados)
	print getTotalOferta(ano)
	print len (getTotalOferta(ano))

	lista.append(Spacer(1,0.6*inch))
	style = styles['Normal']
	headings = ('Data da Contribuição', 'Mês da Contribuição','Total da Contribuição')
	f = getTotalContribuicao(ano)
	
	contribuicao = [(f[i]['dataDaContribuicao'], f[i]['mesDaContribuicao'], f[i]['Total']) for i in range(len(f))]
	tabela = Table([headings] + contribuicao)
	tabela.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
	lista.append(tabela)
	lista.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	dados = Paragraph("%s" %datetime.date.today(), style)
   	lista.append(dados)
   	lista.append(Spacer(1,0.1*inch))
   	dados = Paragraph('O Tesoureiro', style)
	lista.append(dados)
	documento.build(lista, onFirstPage=configuracoesDaPaginaContribuicao)

	return response

def funcionarioPdf(request):
	try:
		ano = request.GET.get('salarioAno')
		mes = request.GET.get('salarioMes')
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')

	response = HttpResponse(content_type='application/pdf')
	doc = SimpleDocTemplate(response)
   	Catalog = []
   	styles = getSampleStyleSheet()
   	style = styles['Heading1']
   	style.alignment = TA_CENTER
   	header = Paragraph("Folha de Salario", style)

   	Catalog.append(header)
   	style = styles['Normal']
   	headings = ('Nome do Funcionario', 'Mês','SS', 'IRT','Faltas','Bonus','Salario Liquido', 'Assinatura')
   	
   	funcionario = [(p.nomeDoFuncionario, p.salarioMes, p.salarioSS, p.salarioIRT, p.salarioNumerodeFaltas, p.salarioBonus, p.salarioLiquido) for p in Salario.objects.filter(salarioAno=ano,salarioMes=mes)]
   	t = Table([headings] + funcionario)
   	t.setStyle(TableStyle(
                      [('GRID', (0,0), (7,7), 1, colors.black),
                       ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey)]))
   	Catalog.append(t) 
   	Catalog.append(Spacer(1,0.2*inch))
   	style = styles['Normal']
   	style.alignment = TA_CENTER
   	p = Paragraph("%s" %datetime.date.today(), style)
   	Catalog.append(p)
   	objeto= Configuracoes.objects.get(pk=1)
   	p= Image(objeto.imagem1, width=100, height=50)
   	Catalog.append(p)
   	
   	doc.build(Catalog)
	return response


def pesquisarDocumento(request):
	informacao = request.GET.get('informacao')
	opcao = request.GET.get('opcao')
	ano = request.GET.get('ano')
	ano = ano

	resultado = ''
	try:
		if opcao =='Numero de Membro' and ano:
			resultado = Membro.objects.get(numeroDeMembro=informacao)
		elif opcao =='Nome':
			resultado = Membro.objects.get(nomeDoMembro=informacao)
		else:
			print ''
	except:
		return HttpResponseRedirect('/gestao/erros/documento/')

	template='pesquisarDocumentoMembro.html'
	igreja = Igreja.objects.last()	 

	return render(request, template, {'resultado':resultado, 'ano':ano, 'igreja':igreja})


def pesquisarDocumentoFinancas(request):
	ano = request.GET.get('ano')
	tipo = request.GET.get('tipo')
	
	resultado = ''

	if ano and tipo =='ofertas':
		resultado = Oferta.objects.filter(anoDaOferta=ano).last
	elif ano and tipo == 'dizimos':
		resultado = Dizimo.objects.filter(anoDoDizimo=ano).last
	elif ano and tipo == 'contribuicoes':
		resultado = Contribuicao.objects.filter(anoDaContribuicao=ano).last
	
		#return HttpResponseRedirect('/gestao/erros/documento/')

	template='pesquisaDocumentoFinancas.html'
	igreja = Igreja.objects.last()
	 

	return render(request, template, {'resultado':resultado,'igreja':igreja})


#_________________________________________Errors_____________________________________

def ErroEliminar(request):
	try:
		if request.session['user']:
			template='erros.html'
			igreja = Igreja.objects.last()
			return render(request, template, {'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')

	

def ErroDocumento(request):
	try:
		if request.session['user']:
			template='errosDocumentos.html'
			igreja = Igreja.objects.last()

			return render(request, template, {'igreja':igreja})
				
	except:
		return HttpResponseRedirect('/login')

	
def SucessoGravacao(request):
	escolha = request.GET.get('escolha')
	escolha1 = request.GET.get('escolha1')
	igreja = Igreja.objects.last()
	template = 'sucessoGravacao.html'
	return render(request, template, {'escolha':escolha, 'escolha1':escolha1, 'igreja':igreja})


#GRAFICOS---------------------------- Nao esquecer a data do membro nos models,formularios e na view homeMembro



def totalDizimos(ano):
	query = connection.cursor()
	query.execute("select sum(valorDoDizimo) as totalDizimo,anoDoDizimo, mesDoDizimo, dataDoDizimo from DjangoOnIis_dizimo where  anoDoDizimo ='%s' group by mesDoDizimo order by field(mesDoDizimo, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')" %ano);
	return dictfetchall(query)

def totalDizimosGeral():
	query = connection.cursor()
	query.execute("select sum(valorDoDizimo) as totalDizimo,anoDoDizimo, mesDoDizimo, dataDoDizimo from DjangoOnIis_dizimo group by mesDoDizimo order by field(mesDoDizimo, 'Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')");
	return dictfetchall(query)

def totalMembros():
	query = connection.cursor()
	query.execute("select count(id) as totalMembros, data as dataMembro from DjangoOnIis_membro group by month(dataMembro) order by dataMembro");
	return dictfetchall(query)



def anos():
	query = connection.cursor()
	query.execute("select distinct anoDoDizimo from DjangoOnIis_dizimo ");
	return dictfetchall(query)

def totalContribuicaoMes(ano):
	query = connection.cursor()
	query.execute("select sum(valorDaContribuicao) as totalContribuicao,anoDaContribuicao, mesDaContribuicao, dataDaContribuicao, descricaoDoProjeto from DjangoOnIis_contribuicao, DjangoOnIis_projeto where DjangoOnIis_projeto.id=DjangoOnIis_contribuicao.descricaoDaContribuicao_id and  anoDaContribuicao ='%s' group by mesDaContribuicao order by anoDaContribuicao" %ano);
	return dictfetchall(query)


def graficos(request):
	try:
		if request.session['user']:
			ano=datetime.date.today().year
        		anoDoDizimo=anos()
        		totaldizimos=totalDizimos(ano)
        		totaloferta=totalOfertaAno(ano)
        		totalcontribuicao=totalContribuicaoMes(ano)
        		totalmembros=totalMembros()
        		opcao = request.GET.get('anoescolha')
        		if opcao:
                		totaldizimos=totalDizimos(opcao)
                		totaloferta=totalOfertaAno(opcao)
                		totalcontribuicao=totalContribuicaoMes(opcao)
                		totalmembros=totalMembros()

                		ano=opcao
       			totaldizimosgeral=totalDizimosGeral()
	
	        	igreja=Igreja.objects.last()
	        	template = 'home.html'
	        	return render(request, template,{'totaldizimos':totaldizimos,'totalmembros':totalmembros,'totaloferta':totaloferta,'totalcontribuicao':totalcontribuicao,'totaldizimosgeral':totaldizimosgeral,'igreja':igreja,'ano':ano,'anoDoDizimo':anoDoDizimo})
				
	except:
		return HttpResponseRedirect('/login')


def usuarios(user,password):
        query = connection.cursor()
        query.execute("select * from DjangoOnIis_utilizador where user='%s' and password='%s' limit 1 "%(user, password));
        return dictfetchall(query)
def usuariosLogin(request):
        template = 'loginUsuarios.html'
        if request.method == 'GET':
        	user = request.GET.get('email')
	        password = request.GET.get('password')
	        resultado = Utilizador.objects.filter(user=user,password=password)
	        if resultado:
	        	resultado = Utilizador.objects.filter(user=user,password=password)

	        	anoDoDizimo=anos()
	        	opcao= datetime.date.today().year
	        	ano=opcao
	        	totaldizimos=totalDizimos(opcao)
	        	totaloferta=totalOfertaAno(opcao)
	        	totalcontribuicao=totalContribuicaoMes(opcao)
	        	totalmembros=totalMembros()
	        	totaldizimosgeral=totalDizimosGeral()
	        	request.session['user']=user
	        	request.session['password']=password
	        	for i in range (len(resultado)):
	        		request.session['id_user'] = resultado[i].nomeDoMembro_id
			igreja=Igreja.objects.last()
	        	template='home.html'
			
			membro=Membro.objects.get(pk=request.session['id_user'])
			request.session['usuario_activo']=str(membro)
			return HttpResponseRedirect('/gestao/')
	        elif request.GET.get('email') and request.GET.get('password'):	
	         	#resultado = Utilizador.objects.all()
	         	resultado='Utilizador ou password incorrectos'
			resultado='Utilizador ou password incorrectos'
	         	return render (request, template,{'resultado':resultado})
	else:
		a=2
	return  render(request, template)	   





def contasDeAcesso(request):
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data['user']
            password = form.cleaned_data['password']
            nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
            new_equipamento, created=Utilizador.objects.get_or_create(nomeDoMembro=nomeDoMembro,password=password,user=user)
            return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=contasdeacesso')
    else:
        form = UsuariosForm()
    template='contasDeAcesso.html'
    try:
    	resultado = Membro.objects.get(pk=request.GET.get('id'))
    except:
	resultado=''
    return render (request, template, {'form':form, 'resultado':resultado})	

def editarContasDeAcesso(request):
        valor = request.GET.get('id')
	request.session['id'] = valor
	try:
		resultado = Utilizador.objects.get(pk=valor)
	except:
		resultado = ''
	if request.method == 'POST':
		form = UsuariosForm(request.POST)
		if form.is_valid():
			user=form.cleaned_data['user']
           		password = form.cleaned_data['password']
            		nomeDoMembro = Membro.objects.get(nomeDoMembro=form.cleaned_data['nomeDoMembro'])
			created = Utilizador.objects.filter(pk=request.session['id']).update(nomeDoMembro=nomeDoMembro,password=password,user=user)
			return HttpResponseRedirect('/gestao/mensagem/sucesso/?escolha=gestao&escolha1=''')

	else:
		form = UsuariosForm()
	membro = Membro.objects.filter(pk=valor)
	template = 'editarContasDeAcesso.html'
	return render(request, template, {'form':form, 'membro':membro,'resultado':resultado})



def get_todos_eventos(tipo):
	query = connection.cursor()
	query.execute("select DjangoOnIis_noticias.*,DjangoOnIis_membro.nomeDoMembro from DjangoOnIis_noticias left join DjangoOnIis_membro on DjangoOnIis_noticias.funcionario_id=DjangoOnIis_membro.id where tipo='%s' order by DjangoOnIis_noticias.dataPublicacao desc " %tipo);
	return dictfetchall(query)


def eventos(request):
	tipo='Evento'
	template = 'eventos.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})

def devocional(request):
	tipo='Devocional'
	template = 'devocional.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})

def musicas(request):
	tipo='Musica'
	template = 'musicas.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})

def discipulado(request):
	tipo='Evangelismo e Missoe'
	template = 'discipulado.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})

def downloads(request):
	tipo='Downloads'
	template = 'downloads.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})

def videos(request):
	tipo='Videos'
	template = 'videos.html'
	resultado = get_todos_eventos(tipo)
	form = NoticiasForm()
	configuracoes = Configuracoes.objects.last()
	igreja = Igreja.objects.last()
	return render(request,template,{'form':form,'resultado':resultado,'configuracoes':configuracoes,'igreja':igreja})



