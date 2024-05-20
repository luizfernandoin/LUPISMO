from app import app, socketio
from ..models.tables import User, Thought, Like, Share
from flask_socketio import emit, send
from flask import render_template, url_for, request, redirect

messages = [] #substitudo do banco de dados.

@app.route("/")
def home():
    return render_template("index.html")

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
    send(messages)