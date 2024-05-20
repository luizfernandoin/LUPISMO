var likeButton = document.querySelector('.like-button');
var shareButton = document.querySelector('.share-button');

window.onload = function() {

    //Instancia socket da função io contendo o servidor.
    const socket = io('http://127.0.0.1:5000');
    
    //Realiza uma coneção da nossa instancia socket, enviando a mensagem para o servidor que o usuario foi conectado. 
    socket.on('connect', () => {
        socket.send('Usuário conectado ao socket!')
    });
    
    //Função que renderizará na tela a mensagem enviada pelo usuario.
    function addToChat(msg) {
        const pensamento = document.querySelector(".thought-main");
        const thoughtContainer = document.createElement('div');
        thoughtContainer.className = 'thought-container';
        thoughtContainer.setAttribute("thought-id", `${msg.id}`);

        thoughtContainer.innerHTML = `
            <div class="thought-header">
                <div class="logo-container">
                    <img src="../static/src/logo.png" alt="Logo do Site">
                </div>
                <h5>Lupismo</h5>
            </div>

            <div class="thought-content">
                <span>${msg.thought}</span>
            </div>

            <div class="thought-footer">
                <div class="author-info">
                    <div class="logo-container">
                        <img src="../static/src/logo.png" alt="Foto do Autor">
                    </div>
                    <span>Luiz Fernando</span>
                </div>
                <div class="action-buttons">
                    <button class="like-button">
                        <i class="bi bi-heart"></i>
                        <span>${msg.likes}</span>
                    </button>
                    <button class="share-button">
                        <i class="bi bi-share"></i>
                        <span>${msg.shares}</span>
                    </button>
                </div>
            </div>
        `;
        pensamento.insertBefore(thoughtContainer, pensamento.firstChild);
        
        thoughtContainer.addEventListener('click', function (event) {
            // Evita que o evento de clique se propague para os elementos pai
            event.stopPropagation();
        
            // Encontra o botão de curtida dentro do pensamento clicado
            const likeButton = this.querySelector('.like-button');
            const shareButton = this.querySelector('.share-button');
            
            // Adiciona ouvintes de eventos para os botões de curtida e compartilhamento
            likeButton.addEventListener('click', function(event) {
                event.stopPropagation();
                toggleIcon(this, 'bi-heart', 'bi-heart-fill');
                socket.emit('likeThought', {'id': msg.id})
            });
        
            shareButton.addEventListener('click', function(event) {
                event.stopPropagation();
                toggleIcon(this, 'bi-share', 'bi-share-fill');
            });
        });
    }

    function addLikes(likes) {
        console.log(likes.likes)
        const thoughtContainer = document.querySelector(`.thought-container[thought-id="${likes.id}"]`);

        if (thoughtContainer) {
            // Encontre os elementos span dentro do thought-container
            const likeSpan = thoughtContainer.querySelector('.like-button span');

            // Defina os valores dos spans
            likeSpan.textContent = likes.likes; // Defina o valor desejado para curtidas
        }
    }

    //Esta selecionando o primeiro form e manipulando o evento de submit através de uma callback(passando uma função como argumento).
    document.querySelector("form").addEventListener("submit", function(event) {
        event.preventDefault(); //Impede que o evento siga seu fluxo normal, refresh.
        
        //Manda uma mensagem para o Backend, no qual sera recebida pela função sendThought, contendo um objeto com as chaves nome e message.
        socket.emit('sendThought', {thought: event.target[0].value})

        //Apos o envio os campos devem ser setados para vázio.
        event.target[0].value = "";
    })

    //Cria um evento da instancia socket (getMessage), responsavel por receber a mensagem do backend. 
    socket.on('getMessage', (msg) => {
        addToChat(msg) //Aciona a função addToChat enviando a mensagem como parametro.
    })

    socket.on('getLike', (likes) => {
        addLikes(likes) //Aciona a função addToChat enviando a mensagem como parametro.
    })


    //recebe do evento message todas as mensagens contidas no array ([{nome: , message: }])
    socket.on('message', (msgs) => {
        for(msg of msgs) {
            addToChat(msg) //chama a função e passa cada mensagem.
        }
    })
}

function toggleIcon(button, firstClass, lastClass) {
    var icon = button.querySelector('i');
    
    // Verifique se o ícone atual é "bi-heart" ou "bi-heart-fill" e alterne-o
    if (icon.classList.contains(firstClass)) {
        icon.classList.remove(firstClass);
        icon.classList.add(lastClass);
    } else {
        icon.classList.remove(lastClass);
        icon.classList.add(firstClass);
    }
}
