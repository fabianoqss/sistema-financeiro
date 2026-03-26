import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.connection import inicializar_banco
from services import usuario_service, transacao_service, categoria_service
from utils.validators import validar_email, validar_valor, validar_data
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'financeiro_secret_2024'

inicializar_banco()


def usuario_logado():
    return 'usuario_id' in session


def get_usuario():
    return {
        'id': session.get('usuario_id'),
        'nome': session.get('usuario_nome'),
        'email': session.get('usuario_email'),
    }


@app.route('/')
def index():
    if not usuario_logado():
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if usuario_logado():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')
        usuario = usuario_service.login(email, senha)
        if usuario:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email
            return redirect(url_for('dashboard'))
        flash('Email ou senha incorretos.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if usuario_logado():
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        if not nome:
            flash('Nome obrigatório.', 'danger')
        elif not validar_email(email):
            flash('Email inválido.', 'danger')
        elif usuario_service.email_ja_cadastrado(email):
            flash('Este email já está cadastrado.', 'danger')
        elif len(senha) < 4:
            flash('Senha deve ter pelo menos 4 caracteres.', 'danger')
        else:
            usuario = usuario_service.cadastrar_usuario(nome, email, senha)
            if usuario:
                categoria_service.criar_categorias_padrao(usuario.id)
                flash('Conta criada com sucesso! Faça login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Erro ao criar conta.', 'danger')
    return render_template('cadastro.html')


@app.route('/dashboard')
def dashboard():
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()
    agora = datetime.now()
    mes, ano = agora.month, agora.year

    saldo = transacao_service.saldo_total(usuario['id'], mes, ano)
    transacoes = transacao_service.listar_transacoes(usuario['id'], mes, ano)[:10]

    for t in transacoes:
        t.data_fmt = datetime.strptime(t.data, '%Y-%m-%d').strftime('%d/%m/%Y')

    return render_template('dashboard.html', usuario=usuario, saldo=saldo,
                           transacoes=transacoes, mes=mes, ano=ano)


@app.route('/extrato')
def extrato():
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()

    mes_str = request.args.get('mes')
    ano_str = request.args.get('ano')

    try:
        mes = int(mes_str) if mes_str else None
        ano = int(ano_str) if ano_str else None
    except ValueError:
        mes, ano = None, None

    transacoes = transacao_service.listar_transacoes(usuario['id'], mes, ano)
    saldo = transacao_service.saldo_total(usuario['id'], mes, ano)

    for t in transacoes:
        t.data_fmt = datetime.strptime(t.data, '%Y-%m-%d').strftime('%d/%m/%Y')

    agora = datetime.now()
    mes_atual = mes or agora.month
    ano_atual = ano or agora.year

    return render_template('extrato.html', usuario=usuario, transacoes=transacoes,
                           saldo=saldo, mes=mes_atual, ano=ano_atual)


@app.route('/lancamento/<tipo>', methods=['GET', 'POST'])
def lancamento(tipo):
    if not usuario_logado():
        return redirect(url_for('login'))
    if tipo not in ('receita', 'despesa'):
        return redirect(url_for('dashboard'))

    usuario = get_usuario()
    categorias = categoria_service.listar_categorias(usuario['id'], tipo)

    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        valor_str = request.form.get('valor', '')
        data_str = request.form.get('data', '')
        categoria_id_str = request.form.get('categoria_id', '0')

        valor = validar_valor(valor_str)
        data = validar_data(data_str) if data_str else datetime.now().strftime('%Y-%m-%d')
        categoria_id = int(categoria_id_str) if categoria_id_str and categoria_id_str != '0' else None

        if not descricao:
            flash('Descrição obrigatória.', 'danger')
        elif valor is None:
            flash('Valor inválido.', 'danger')
        else:
            t = transacao_service.adicionar_transacao(
                descricao, valor, tipo, data, categoria_id, usuario['id']
            )
            if t:
                flash(f'{"Receita" if tipo == "receita" else "Despesa"} lançada com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Erro ao registrar lançamento.', 'danger')

    hoje = datetime.now().strftime('%Y-%m-%d')
    return render_template('lancamento.html', usuario=usuario, tipo=tipo,
                           categorias=categorias, hoje=hoje)


@app.route('/transacao/excluir/<int:tid>', methods=['POST'])
def excluir_transacao(tid):
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()
    ok = transacao_service.excluir_transacao(tid, usuario['id'])
    flash('Transação excluída.' if ok else 'Transação não encontrada.', 'success' if ok else 'danger')
    return redirect(request.referrer or url_for('extrato'))


@app.route('/categorias')
def categorias():
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()
    cats = categoria_service.listar_categorias(usuario['id'])
    return render_template('categorias.html', usuario=usuario, categorias=cats)


@app.route('/categorias/nova', methods=['POST'])
def nova_categoria():
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()
    nome = request.form.get('nome', '').strip()
    tipo = request.form.get('tipo', '')

    if not nome:
        flash('Nome obrigatório.', 'danger')
    elif tipo not in ('receita', 'despesa'):
        flash('Tipo inválido.', 'danger')
    else:
        cat = categoria_service.criar_categoria(nome, tipo, usuario['id'])
        if cat:
            flash(f'Categoria "{nome}" criada.', 'success')
        else:
            flash('Erro ao criar categoria.', 'danger')
    return redirect(url_for('categorias'))


@app.route('/categorias/excluir/<int:cid>', methods=['POST'])
def excluir_categoria(cid):
    if not usuario_logado():
        return redirect(url_for('login'))
    usuario = get_usuario()
    ok = categoria_service.excluir_categoria(cid, usuario['id'])
    if ok:
        flash('Categoria excluída.', 'success')
    else:
        flash('Não é possível excluir: categoria possui transações vinculadas.', 'danger')
    return redirect(url_for('categorias'))


if __name__ == '__main__':
    app.run(debug=True)
