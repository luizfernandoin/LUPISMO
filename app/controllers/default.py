from app import app, socketio, db
from ..models.tables import User, Thought, Like, Share
from flask_socketio import emit, send
from flask import render_template, url_for, request, redirect, flash, session, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import time
import os

messages = [] 

@app.route("/")
def feed():
    thoughts = Thought.query.order_by(Thought.created_at.desc()).all()
    user_id = session.get('user_id')

    return render_template("index.html", thoughts=thoughts, user_id=user_id)

@app.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    thoughts = Thought.query.filter_by(author_id=user.id).all()
    
    return render_template('profile.html', user_id=user.id, thoughts=thoughts)

@app.route('/users/<int:user_id>/thoughts', methods=['GET'])
def get_user_thoughts(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    thoughts = Thought.query.filter_by(author_id=user_id).all()
    
    return render_template('profile.html', user_id=user.id, thoughts=thoughts)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signIn.html")
    
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
        return redirect(url_for('feed'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signUp.html")

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
        session['user_id'] = new_user.id
        
        profile = request.files['capa']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        profile.save(f'{upload_path}/profile{new_user.id}-{timestamp}.jpg')
        
        flash('User registered successfully. You can now login.', 'success')
        return redirect(url_for('feed'))

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/thought', methods=['GET'])
def get_thought():
    thoughts = Thought.query.all()
    return jsonify([thought.to_dict() for thought in thoughts]), 200

@socketio.on('addThought')
def add_thought(data):
    text = data['thought']

    if not text:
        flash('Texto do pensamento não pode ser vazio.', 'error')
        return redirect(url_for('feed'))  # Ou qualquer rota que faça sentido

    # Obtém o ID do usuário autenticado
    user_id = session.get('user_id')

    # Verifica se o usuário está autenticado
    if not user_id:
        flash('Usuário não autenticado.', 'error')
        return redirect(url_for('feed'))  # Ou qualquer rota que faça sentido

    # Cria um novo pensamento
    new_thought = Thought(
        text=text,
        author_id=user_id
    )

    # Adiciona o pensamento ao banco de dados
    db.session.add(new_thought)
    db.session.commit()

    flash('Pensamento adicionado com sucesso!', 'success')
    
    profile_image = recupera_imagem(new_thought.author_id)
    if profile_image:
        profile_url = url_for('imagem', nome_arquivo=profile_image)
    else:
        profile_url = url_for('static', filename='src/profile.png')
    
    thought_data = {
        'id': new_thought.id,
        'thought': new_thought.text,
        'author': new_thought.author.username,
        'likes': 0,
        'shares': 0,
        'time': new_thought.time_since_posted(),
        'profile': profile_url
    }

    
    print(thought_data)
    # Emite a mensagem para todos os clientes conectados
    emit('getMessage', thought_data, broadcast=True)
    
@socketio.on('likeThought')
def like_thought(data):
    thought_id = data['id']
    user_id = session.get('user_id')
    existing_like = Like.query.filter_by(user_id=user_id, thought_id=thought_id).first()
    
    if user_id:
        if existing_like:
            db.session.delete(existing_like)
            db.session.commit()
        
            thought = Thought.query.get(thought_id)
            thought.decrement_likes()

            print(thought)
            
            socketio.emit('updateLikes', {'increment': False, 'id': thought_id, 'likes': thought.likes_count})
        else:
            new_like = Like(user_id=user_id, thought_id=thought_id)
            db.session.add(new_like)
            db.session.commit()
            
            thought = Thought.query.get(thought_id)
            thought.increment_likes()
            
            socketio.emit('updateLikes', {'increment': True, 'id': thought_id, 'likes': thought.likes_count})

@socketio.on('getTimePosted')
def get_time_posted():
    thoughts = Thought.query.all()
    
    thought_data = []
    
    for thought in thoughts:
        thought_data.append({
            'id': thought.id,
            'created_at': thought.time_since_posted()
        })

    socketio.emit('updateTimePosted', thought_data)

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory(app.config['UPLOAD_PATH'], nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'profile{id}' in nome_arquivo:
            return nome_arquivo
    return None 

@app.route('/visualiza/<int:id>')
def visualiza_imagem(id):
    capa = recupera_imagem(id)
    if capa:
        return imagem(capa)
    else:
        flash('Imagem não encontrada', 'error')
        return redirect(url_for('feed'))
    
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    user_id = session.get('user_id')
    
    thought_results = []
    user_results = []
    if query:
        thought_results = Thought.query.filter(Thought.text.ilike(f'%{query}%')).all()
        user_results = User.query.filter(User.username.ilike(f'%{query}%')).all()
        
    return render_template('search.html', query=query, thoughts=thought_results, users=user_results, user_id=user_id)
