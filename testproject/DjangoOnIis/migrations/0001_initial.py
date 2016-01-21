# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('autor', models.CharField(max_length=100)),
                ('comentario', models.CharField(max_length=5000)),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Configuracoes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imagem1', models.ImageField(upload_to=b'fotos/%Y/%m/%d')),
                ('imagem2', models.ImageField(upload_to=b'fotos/%Y/%m/%d')),
                ('texto1', models.CharField(max_length=400)),
                ('texto2', models.CharField(max_length=400)),
                ('texto3', models.CharField(max_length=400)),
                ('texto4', models.CharField(max_length=400)),
                ('texto5', models.CharField(max_length=400)),
                ('texto6', models.CharField(max_length=400)),
                ('desenvolvedores', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Contribuicao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valorDaContribuicao', models.FloatField(default=None)),
                ('dataDaContribuicao', models.DateField()),
                ('mesDaContribuicao', models.CharField(max_length=20)),
                ('anoDaContribuicao', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDoDepartamento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dizimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valorDoDizimo', models.FloatField(default=None)),
                ('dataDoDizimo', models.DateField()),
                ('mesDoDizimo', models.CharField(max_length=20)),
                ('anoDoDizimo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=50)),
                ('numeroDeSerie', models.CharField(max_length=30)),
                ('dataDaAquisicao', models.DateField()),
                ('modelo', models.CharField(max_length=30)),
                ('localizacao', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=30)),
                ('preco', models.FloatField(default=None)),
                ('obs', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evento', models.CharField(max_length=5000)),
                ('dataDoEvento', models.DateField()),
                ('localDoEvento', models.CharField(max_length=200)),
                ('autor', models.CharField(max_length=100)),
                ('dataDaPublicacao', models.DateField()),
                ('departamento', models.ForeignKey(to='DjangoOnIis.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDoFuncionario', models.CharField(max_length=100)),
                ('estadoCivil', models.CharField(max_length=20)),
                ('sexo', models.CharField(max_length=10)),
                ('cargo', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('caixaPostal', models.CharField(max_length=10)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('dataDeNascimento', models.DateField()),
                ('grauAcademico', models.CharField(max_length=50)),
                ('profissao', models.CharField(max_length=50)),
                ('numeroDeIdentificacao', models.CharField(max_length=50)),
                ('filiacaoPai', models.CharField(max_length=100)),
                ('filiacaoMae', models.CharField(max_length=100)),
                ('numeroDeFuncionario', models.CharField(max_length=20)),
                ('salarioBase', models.FloatField(default=None)),
                ('foto', models.ImageField(null=True, upload_to=b'fotos/%Y/%m/%d', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Igreja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDaIgreja', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('caixaPostal', models.CharField(max_length=10)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('dataDeCriacao', models.DateField()),
                ('logotipo', models.ImageField(default=b'fotos/no-img.jpg', upload_to=b'fotos/')),
            ],
        ),
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDoMembro', models.CharField(max_length=100)),
                ('estadoCivil', models.CharField(max_length=20)),
                ('sexo', models.CharField(max_length=10)),
                ('cargo', models.CharField(max_length=50)),
                ('funcaoNaIgreja', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('caixaPostal', models.CharField(max_length=10)),
                ('telefone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=200)),
                ('dataDeNascimento', models.DateField()),
                ('grauAcademico', models.CharField(max_length=50)),
                ('profissao', models.CharField(max_length=50)),
                ('numeroDeIdentificacao', models.CharField(max_length=50)),
                ('conjuge', models.CharField(max_length=100)),
                ('filiacaoPai', models.CharField(max_length=100)),
                ('filiacaoMae', models.CharField(max_length=100)),
                ('dataDeConversao', models.DateField(null=True, blank=True)),
                ('procedencia', models.CharField(max_length=100)),
                ('formaDeAdmissao', models.CharField(max_length=50)),
                ('dataDeBaptismo', models.DateField(null=True, blank=True)),
                ('localDeBaptismo', models.CharField(max_length=50, null=True, blank=True)),
                ('dataDeConsagracaoDiacono', models.DateField(null=True, blank=True)),
                ('dataDeConsagracaoEvangelista', models.DateField(null=True, blank=True)),
                ('dataDeConsagracaoPastor', models.DateField(null=True, blank=True)),
                ('dataDeConsagracaoMissionario', models.DateField(null=True, blank=True)),
                ('numeroDeMembro', models.CharField(max_length=20)),
                ('data', models.DateField()),
                ('foto', models.ImageField(null=True, upload_to=b'fotos/%Y/%m/%d', blank=True)),
                ('departamento', models.ForeignKey(to='DjangoOnIis.Departamento')),
                ('igreja', models.ForeignKey(to='DjangoOnIis.Igreja')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDoMunicipio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Noticias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=300)),
                ('noticia', models.CharField(max_length=5000)),
                ('foto', models.ImageField(upload_to=b'fotos/%Y/%m/%d')),
                ('dataPublicacao', models.DateField()),
                ('tipo', models.CharField(max_length=20)),
                ('funcionario', models.ForeignKey(to='DjangoOnIis.Membro')),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valorDaOferta', models.FloatField(default=None)),
                ('dataDaOferta', models.DateField()),
                ('mesDaOferta', models.CharField(max_length=20)),
                ('anoDaOferta', models.CharField(max_length=10)),
                ('igreja', models.ForeignKey(to='DjangoOnIis.Igreja')),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDoPais', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diaDaSemana', models.CharField(max_length=25)),
                ('descricao', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricaoDoProjeto', models.CharField(max_length=300)),
                ('orcamento', models.FloatField(default=None)),
                ('igreja', models.ForeignKey(to='DjangoOnIis.Igreja')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomeDaProvincia', models.CharField(max_length=50)),
                ('idDoPais', models.ForeignKey(to='DjangoOnIis.Pais')),
            ],
        ),
        migrations.CreateModel(
            name='Salario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salarioAno', models.CharField(max_length=10)),
                ('salarioMes', models.CharField(max_length=20)),
                ('salarioSS', models.FloatField(default=None)),
                ('salarioIRT', models.FloatField(default=None)),
                ('salarioNumerodeFaltas', models.CharField(max_length=10)),
                ('salarioBonus', models.FloatField(max_length=100)),
                ('salarioLiquido', models.FloatField(default=None)),
                ('nomeDoFuncionario', models.ForeignKey(to='DjangoOnIis.Funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userEmail', models.EmailField(max_length=100)),
                ('userPassword', models.CharField(max_length=100)),
                ('funcionario', models.ForeignKey(to='DjangoOnIis.Funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('nomeDoMembro', models.ForeignKey(to='DjangoOnIis.Membro')),
            ],
        ),
        migrations.AddField(
            model_name='municipio',
            name='idDaProvincia',
            field=models.ForeignKey(to='DjangoOnIis.Provincia'),
        ),
        migrations.AddField(
            model_name='membro',
            name='pais',
            field=models.ForeignKey(to='DjangoOnIis.Pais'),
        ),
        migrations.AddField(
            model_name='membro',
            name='provincia',
            field=models.ForeignKey(to='DjangoOnIis.Provincia'),
        ),
        migrations.AddField(
            model_name='igreja',
            name='cidade',
            field=models.ForeignKey(to='DjangoOnIis.Municipio'),
        ),
        migrations.AddField(
            model_name='igreja',
            name='provincia',
            field=models.ForeignKey(to='DjangoOnIis.Provincia'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='pais',
            field=models.ForeignKey(to='DjangoOnIis.Pais'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='provincia',
            field=models.ForeignKey(to='DjangoOnIis.Provincia'),
        ),
        migrations.AddField(
            model_name='eventos',
            name='igreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='equipamento',
            name='igreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='dizimo',
            name='igreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='dizimo',
            name='nomeDoMembro',
            field=models.ForeignKey(to='DjangoOnIis.Membro'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='idDaIgreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='contribuicao',
            name='descricaoDaContribuicao',
            field=models.ForeignKey(to='DjangoOnIis.Projeto'),
        ),
        migrations.AddField(
            model_name='contribuicao',
            name='igreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='contribuicao',
            name='nomeDoMembro',
            field=models.ForeignKey(to='DjangoOnIis.Membro'),
        ),
        migrations.AddField(
            model_name='configuracoes',
            name='igreja',
            field=models.ForeignKey(to='DjangoOnIis.Igreja'),
        ),
        migrations.AddField(
            model_name='comentarios',
            name='noticia',
            field=models.ForeignKey(to='DjangoOnIis.Noticias'),
        ),
    ]
