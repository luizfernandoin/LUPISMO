import { socket } from "./socket.js";

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
                <div class="author-profile">
                    <div class="logo-container">
                        <img src="${msg.profile}" alt="Foto do Autor">
                    </div>
                </div>
                <div class="author-info">
                    <p>${msg.author}</p>
                    <span class="post-time">${msg.time}</span>
                </div>
            </div>

            <div class="thought-content">
                <span>${msg.thought}</span>
            </div>

            <div class="thought-footer">
                <div class="action-buttons">
                    <button class="like-button">
                        <i class="bi bi-heart"></i>
                        <span>${msg.likes}</span>
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

//Cria um evento da instancia socket (getMessage), responsavel por receber a mensagem do backend. 
socket.on('getMessage', (msg) => {
    addToChat(msg) //Aciona a função addToChat enviando a mensagem como parametro.
})