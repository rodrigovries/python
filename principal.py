# principal.py
from flask import Flask, render_template, request, url_for, redirect, session, flash

from dao import ProdutoDao
from produto import Produto

produto_dao = ProdutoDao('bancodados.db')

app = Flask(__name__)
app.secret_key = 'softgraf'

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    lista = produto_dao.listar()
    return render_template('relatorio.html', titulo='relatório de estoque', produtos=lista)

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect(url_for('index'))

@app.route('/cadastrar')
def cadastrar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    return render_template('cadastrar.html', titulo='cadastro de produtos')

@app.route('/salvar', methods=['POST'])
def salvar():
    id = request.form['id']
    descricao = request.form['descricao']
    preco = request.form['preco']
    quantidade = request.form['quantidade']
    produto = Produto(descricao, preco, quantidade, id)
    produto_dao.salvar(produto)
    return redirect(url_for('index'))

@app.route('/editar/<string:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    produto = produto_dao.buscar_por_id(id)
    return render_template('editar.html', titulo='Edição de produto', produto=produto)

@app.route('/deletar/<string:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    produto_dao.deletar(id)
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['senha'] == '123':
        session['usuario_logado'] = request.form['usuario']
        flash(request.form['usuario'] + ' logou com sucesso')
        return redirect(url_for('index'))
    else:
        flash('Senha Invalida')
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
