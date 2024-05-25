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
        if (!pensamento) {
            console.error("Element with class 'thought-main' not found.");
            return;
        }
    
        const thoughtContainer = document.createElement('div');
        thoughtContainer.className = 'thought-container';
        thoughtContainer.setAttribute("thought-id", `${msg.id}`);
    
        thoughtContainer.innerHTML = `
            <div class="card-thought">
                <div class="thought-header">
                    <div class="logo-container">
                        <img src="../static/src/logo.png" alt="Logo do Site">
                    </div>
                    <div>
                        <h5>Lupismo</h5>
                        <span>${msg.time}</span>
                    </div>
                </div>

                <div class="thought-content">
                    <span>${msg.thought}</span>
                </div>

                <div class="thought-footer">
                    <div class="author-info">
                        <div class="logo-container">
                            <img src="../static/src/logo.png" alt="Foto do Autor">
                        </div>
                        <span>${msg.author}</span>
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
            </div>
        `;
    
        if (pensamento.firstChild) {
            pensamento.insertBefore(thoughtContainer, pensamento.firstChild);
        } else {
            pensamento.appendChild(thoughtContainer);
        }
    }

    //Esta selecionando o primeiro form e manipulando o evento de submit através de uma callback(passando uma função como argumento).
    document.querySelector("form").addEventListener("submit", function(event) {
        event.preventDefault(); //Impede que o evento siga seu fluxo normal, refresh.
        const editableDiv = document.getElementById('thought');
        const thoughtText = editableDiv.innerText.trim();

        //Manda uma mensagem para o Backend, no qual sera recebida pela função sendThought, contendo um objeto com as chaves nome e message.
        socket.emit('addThought', {thought: thoughtText})

        //Apos o envio os campos devem ser setados para vázio.
        editableDiv.innerText = "";
    })

    //Cria um evento da instancia socket (getMessage), responsavel por receber a mensagem do backend. 
    socket.on('getMessage', (msg) => {
        addToChat(msg) //Aciona a função addToChat enviando a mensagem como parametro.
    })

    //recebe do evento message todas as mensagens contidas no array ([{nome: , message: }])
    socket.on('message', (msgs) => {
        for(msg of msgs) {
            addToChat(msg) //chama a função e passa cada mensagem.
        }
    })

    socket.on('updateLikes', function(data_like) {
        console.log(data_like.likes)
        const thoughtContainer = document.querySelector(`.thought-container[thought-id="${data_like.id}"]`);
    
        if (thoughtContainer) {
            const button = thoughtContainer.querySelector('.like-button');
            
            if (data_like.increment) {
                toggleIcon(button, 'bi-heart', 'bi-heart-fill');
            } else {
                toggleIcon(button, 'bi-heart-fill', 'bi-heart');
            }
    
            const likeSpan = thoughtContainer.querySelector('.like-button span');
            likeSpan.textContent = data_like.likes;
        }
    });

    document.querySelector(".thought-main").addEventListener("click", function(event) {
        const thoughtContainer = event.target.closest('.thought-container');
        if (!thoughtContainer) return;

        const thoughtId = thoughtContainer.getAttribute('thought-id');

        if (event.target.closest('.like-button')) {
            event.stopPropagation();
            socket.emit('likeThought', { id: thoughtId });
        }

        if (event.target.closest('.share-button')) {
            event.stopPropagation();
            const button = event.target.closest('.share-button');
            toggleIcon(button, 'bi-share', 'bi-share-fill');
        }
    });

    socket.on('updateTimePosted', (data) => {
        data.forEach((timeData) => {
            console.log(timeData)
            const postTimeElement = document.querySelector(`.thought-container[thought-id="${timeData.id}"] .post-time`);
            if (postTimeElement) {
                postTimeElement.textContent = timeData.created_at;
            }
        });
    })
    
    setInterval(() => {
        socket.emit('getTimePosted')
    }, 60000);
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
