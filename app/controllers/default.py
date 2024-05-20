from app import app, socketio, db
from ..models.tables import User, Thought, Like, Share
from flask_socketio import emit, send
from flask import render_template, url_for, request, redirect, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

messages = [] 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('signin'))

        # Cria uma sessão para o usuário autenticado
        session['user_id'] = user.id
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        # Verifica se o email já está registrado
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('signup'))

        # Cria o novo usuário
        new_user = User(
            username=username,
            email=email,
            password=password
        )

        # Adiciona o usuário ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully. You can now login.', 'success')
        return redirect(url_for('home'))

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.__dict__ for user in users]), 200



"""
@app.route("/autenticar", methods=['POST'])
def autenticar():


@app.route("/create_user", methods=['POST'])
def create_user():
   """ 

"""
@app.route('/criar', methods=['POST',])
def criar():
    title = request.form['nome']
    overview = request.form['overview']
    avaliacao = request.form['avaliacao']
    tot_avaliacao = request.form['tot_avaliacao']

    movie = Movies.query.filter_by(title=title).first()

    if movie:
        flash('Filme já existente!')
        return redirect(url_for('index'))

    novo_movie = Movies(id=None, title=title,overview=overview,poster='False',vote_average=avaliacao,vote_count=tot_avaliacao)

    db.session.add(novo_movie)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    capa.save(f'{upload_path}/capa{novo_movie.id}-{timestamp}.jpg')


    flash('Filme criado com sucesso!')
    return redirect(url_for('index'))



#Função que recebe a mensagem enviada pelo usuario.
@socketio.on('sendMessage')
def send_message_handler(msg):
    messages.append(msg) #adiciona a mensagem ao banco de dados (um array).
    emit('getMessage', msg, broadcast=True) #emite para o Frontend(usuario) através do evento getMessage, eviando como argumento a mensagem em formato broadcast(para todos);


#Função que envia o array messages para o front através do evento message.
@socketio.on('message')
def handle_message(msg):
    send(messages)"""