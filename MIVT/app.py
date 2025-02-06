import os
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, url_for, render_template, request, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Configure application
app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///loja.db")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

users = {}

# Inicializar o carrinho na sessão
@app.before_request
def before_request():
    if 'carrinho' not in session:
        session['carrinho'] = []
    if 'pedidos' not in session:
        session['pedidos'] = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    # Consultar todos os produtos do banco de dados
    produtos = db.execute("SELECT * FROM produtos")
    produtos_exibidos = produtos

    if request.method == 'POST':
        if 'produto_id' in request.form:
            produto_id = int(request.form['produto_id'])
            quantidade = int(request.form['quantidade'])

            # Buscar o produto com base no produto_id
            produto = db.execute("SELECT * FROM produtos WHERE id = ?", produto_id)

            if produto:
                produto = produto[0]  # Obter o primeiro (e único) resultado
                user = db.execute("SELECT * FROM users WHERE username = ?", username)
                carrinho = json.loads(user[0]['carrinho'])
                carrinho.append({'id': produto_id, 'quantidade': quantidade, 'preco': produto['preco'], 'nome': produto['nome']})

                db.execute("UPDATE users SET carrinho = ? WHERE username = ?", json.dumps(carrinho), username)
                flash('Product added to cart!', 'success')

        elif 'busca' in request.form:  # Realizando busca
            busca = request.form['busca'].lower()
            produtos_exibidos = db.execute("SELECT * FROM produtos WHERE LOWER(nome) LIKE ?", f"%{busca}%")

    return render_template('index.html', user=session['user'], produtos=produtos_exibidos)


@app.route('/carrinho')
def carrinho():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    # Buscar o carrinho do banco de dados
    user = db.execute("SELECT * FROM users WHERE username = ?", username)
    carrinho = json.loads(user[0]['carrinho'])  # Carrinho armazenado como JSON

    # Calcular o valor total do carrinho, verificando se todos os produtos têm 'preco' e 'quantidade'
    total = sum(produto['preco'] * produto['quantidade']
                for produto in carrinho
                    if 'preco' in produto and 'quantidade' in produto)

    return render_template('carrinho.html', carrinho=carrinho, total=total)


@app.route('/remover', methods=['POST'])
def remover():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    produto_id = int(request.form['produto'])  # ID do produto enviado no formulário
    quantidade_remover = int(request.form['quantidade'])  # Quantidade a ser removida

    # Buscar o carrinho do banco de dados
    user = db.execute("SELECT * FROM users WHERE username = ?", username)
    carrinho = json.loads(user[0]['carrinho'])  # Carrinho armazenado como JSON

    # Verificar e remover o item correspondente
    for produto in carrinho:
        if produto['id'] == produto_id and produto['quantidade'] == quantidade_remover:
            carrinho.remove(produto)
            flash(f"'{produto['nome']}' removed from cart!", 'success')
            break  # Sai do loop após encontrar e remover o item

    # Salvar as alterações no banco de dados
    db.execute("UPDATE users SET carrinho = ? WHERE username = ?", json.dumps(carrinho), username)

    return redirect('/carrinho')  # Redireciona para a página do carrinho


@app.route('/compra', methods=['GET', 'POST'])
def compra():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

     # Criar a lista de produtos com quantidades e subtotais
    user = db.execute("SELECT * FROM users WHERE username = ?", username)
    carrinho = json.loads(user[0]['carrinho'])  # Carrinho armazenado como JSON

    if request.method == 'GET':
        # Verificar se o carrinho está vazio
        if not carrinho:
            flash("Your cart is empty.", "error")
            return redirect('/carrinho')
        else:
            return render_template('compra.html')

    # Obter os dados do formulário
    endereco = request.form.get('endereco')
    metodo_pagamento = request.form.get('metodo_pagamento')

    # Capturar o momento atual
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    produtos_com_quantidade = []
    for produto in carrinho:
        produtos_com_quantidade.append({
            'nome': produto['nome'],
            'preco': produto['preco'],
            'quantidade': produto['quantidade'],
            'subtotal': produto['preco'] * produto['quantidade']
        })

    # Criar o pedido
    pedido = {
        'produtos': produtos_com_quantidade,
        'endereco': endereco,
        'metodo_pagamento': metodo_pagamento,
        'data_hora': data_hora
    }

    # Buscar os pedidos existentes
    pedidos_existentes = json.loads(user[0]['pedidos'])  # Pedidos armazenados como JSON

    # Adicionar o novo pedido à lista de pedidos
    pedidos_existentes.append(pedido)

    # Atualizar o banco de dados para adicionar o novo pedido e limpar o carrinho
    db.execute("UPDATE users SET pedidos = ?, carrinho = ? WHERE username = ?",
               json.dumps(pedidos_existentes), json.dumps([]), username)

    return redirect('/pedidos')


@app.route('/pedidos')
def pedidos():
    if 'user' not in session:
        return redirect('/login')

    username = session['user']

    # Buscar os pedidos no banco de dados
    user = db.execute("SELECT * FROM users WHERE username = ?", username)
    pedidos = json.loads(user[0]['pedidos'])  # Pedidos armazenados como JSON

    # Calcular o subtotal de cada produto e o total do pedido
    for pedido in pedidos:
        for produto in pedido['produtos']:
            produto['subtotal'] = produto['preco'] * produto['quantidade']

        pedido['total'] = sum(produto['subtotal'] for produto in pedido['produtos'])

    return render_template('pedidos.html', pedidos=pedidos)


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Consultar o banco para verificar se o usuário existe
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        if user and check_password_hash(user[0]['password'], password):
            session['user'] = username
            session['carrinho'] = []  # Inicializar carrinho vazio
            session['pedidos'] = []   # Inicializar pedidos vazio
            return redirect('/')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário já existe
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        if user:
            flash('User already registered!', 'warning')
        else:
            db.execute("INSERT INTO users (username, password, carrinho, pedidos) VALUES (?, ?, ?, ?)",
                       username, generate_password_hash(password), json.dumps([]), json.dumps([]))
            flash('Registration successful!', 'success')
            return redirect('/login')

    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully exited!', 'info')

    return redirect('/login')

@app.route('/login_comerciante', methods=['GET', 'POST'])
def login_comerciante():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Consultar o banco para verificar se o comerciante existe
        comerciante = db.execute("SELECT * FROM comerciantes WHERE username = ?", username)

        if comerciante and check_password_hash(comerciante[0]['password'], password):
            session['comerciante'] = username
            return redirect('/adicionar_produto')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login_comerciante.html')


@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        imagem = request.files['imagem']

        if imagem:
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Salve os detalhes no banco de dados
            db.execute("INSERT INTO produtos (nome, preco, imagem) VALUES (?, ?, ?)",
                       nome, preco, filename)

            flash("Product added successfully!", "success")
            return redirect('/adicionar_produto')

    return render_template('adicionar_produto.html')


@app.route('/logout_comerciante')
def logout_comerciante():
    session.pop('comerciante', None)
    flash('You have successfully exited!', 'info')
    return redirect('/login')

