from flask import Flask, json,jsonify,request, render_template, redirect, url_for,session,flash, Markup, abort, send_file
from random import randint
import os
import glob
import ast 
import json
import time
from database import db
from models import *

app = Flask(__name__)
app.config.from_object('config')

# Inicializa a instancia do banco dentro do contexto da aplicacao
db.init_app(app)

# p/ forçar reload do css e js no navegador quando server atualizado
unixtime = int(time.time()) 

@app.route('/')
def home():
    if not session.get('logged'):
        return render_template('home.html',unixtime=unixtime)
    ficha = db.session.query(Ficha).filter_by(id=session['id_da_ficha']).first()
    return render_template('home.html',unixtime=unixtime,ficha=ficha,session=session)

@app.route('/ficha/upload-json/', methods=['GET', 'POST'])
def upload_json():
    if request.method == 'GET':
        if session.get('logged'):
            return redirect(url_for("listar_ficha"))
        else:
            return render_template('upload_json.html',unixtime=unixtime)
    ficha = Ficha()
    # TODO: adequar ao curso
    ficha.meta_das_obrigatorias = 90
    ficha.meta_das_limitadas = 57
    ficha.meta_das_livres = 43
    db.session.add(ficha)
    db.session.commit() # p/ ter id (autoincrement)
    codigos_ignorados = ['ATC-BCT','ATC-BCH','TRT']
    registros = json.loads(request.files['jsonfile'].read().decode('utf8'))
    for registro in registros:
        if not registro['codigo'].upper() in codigos_ignorados:
            disciplina = Disciplina()
            disciplina.ficha_id = ficha.id
            disciplina.codigo = str(registro['codigo'])
            disciplina.nome = str(registro['disciplina'])
            disciplina.creditos = registro['creditos']
            disciplina.ano = registro['ano']
            disciplina.periodo = str(registro['periodo'])
            disciplina.conceito = str(registro['conceito'])
            disciplina.situacao = str(registro['situacao'])
            disciplina.categoria = str(registro['categoria'])
            db.session.add(disciplina)
    if len(ficha.disciplinas) > 0:
        ficha.calcula_coeficientes()
    db.session.commit()
    session['logged'] = True
    session['id_da_ficha'] = ficha.id
    return redirect(url_for("listar_ficha"))

@app.route('/ficha/listar/',methods=['GET'])
def listar_ficha():
    if not session.get('logged'):
        return redirect(url_for("home"))
    ficha = Ficha.query.filter_by(id=session['id_da_ficha']).first()
    return render_template('listar_ficha.html',unixtime=unixtime,ficha=ficha,session=session) 

@app.route('/ficha/atualizar/disciplina/', methods=["POST"])
def ficha_atualizar_disciplina():
    if not session.get('logged'):
        return json.dumps({'info':'user not logged'}), 401, {'ContentType':'application/json'} 
    data = request.get_json(force=True, silent=False, cache=False)
    ficha = db.session.query(Ficha).filter_by(id=session['id_da_ficha']).first()
    for disciplina in ficha.disciplinas:
        if disciplina.codigo == data['codigo'] and disciplina.ano == data['ano'] and disciplina.periodo == data['periodo']:
            disciplina.conceito = data['conceito']
            disciplina.verifica_situacao()
            db.session.add(disciplina)
            print("Atualizado disciplina %s para o conceito %s"%(disciplina.nome,disciplina.conceito))
    ficha.calcula_coeficientes()
    db.session.add(ficha)
    db.session.commit()
    return json.dumps({'info':'disciplina atualizada'}), 200, {'ContentType':'application/json'} 

@app.route('/ficha/inserir-disciplina/',methods=['GET'])
def inserir_disciplina():
    if not session.get('logged'):
        return redirect(url_for('login'))
    aluno = Aluno()
    aluno.login = session['login']
    return render_template('inserir_disciplina.html',aluno=aluno)   

@app.route('/ficha/inserir/disciplina/', methods=["POST"])
def ficha_inserir_disciplina():
    if not session.get('logged'):
        return json.dumps({'info':'user not logged'}), 401, {'ContentType':'application/json'} 
    data = request.get_json(force=True, silent=False, cache=False)
    ficha = db.session.query(Ficha).filter_by(id=session['id_da_ficha']).first()
    disciplina = Disciplina()
    disciplina.codigo = data['codigo']
    disciplina.ano = data['ano']
    disciplina.periodo = data['periodo']
    disciplina.nome = data['nome']
    disciplina.creditos = data['creditos']
    disciplina.categoria = data['categoria']
    disciplina.conceito = data['conceito']
    disciplina.verifica_situacao()
    if not Disciplina.query.filter_by(codigo=disciplina.codigo,ano=disciplina.ano,periodo=disciplina.periodo).first():
        ficha.disciplinas.append(disciplina)
        ficha.calcula_coeficientes()
        db.session.add(ficha)
        db.session.commit()
        print("Adicionado disciplina %s"%(disciplina.nome))
    return json.dumps({'info':'disciplina inserida'}), 200, {'ContentType':'application/json'} 


@app.route('/ficha/listar-disciplina/',methods=['POST'])
def listar_disciplina():
    if not session.get('logged'):
        return redirect(url_for('login'))
    aluno = Aluno()
    aluno.login = session['login']
    parametros = request.form.get('disciplina')
    parametros = parametros.replace('(','').replace(')','').replace("'",'').strip().split(',')
    disciplina = Disciplina()
    disciplina.codigo = parametros[0]
    disciplina.ano = parametros[1]
    disciplina.periodo = parametros[2]
    disciplina.record = session['record']
    disciplina = DisciplinaDAO().listar_por_codigo_ano_periodo(disciplina)
    return render_template('listar_disciplina.html',disciplina=disciplina,aluno=aluno)       

@app.route('/logout')
def logout():
    session.clear()
    message = Markup("logout realizado")
    flash(message,'info')
    return redirect(url_for('home'))