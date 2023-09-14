var likeButton = document.querySelector('.like-button');
var shareButton = document.querySelector('.share-button');

window.onload = function() {

    //Instancia socket da função io contendo o servidor.
    const socket = io('http://127.0.0.1:5000');

    //Função que renderizará na tela a mensagem enviada pelo usuario.
    function addToChat(msg) {
        const span = document.createElement("span");
        const pensamento = document.querySelector(".content-pensamento");
        span.innerHTML = `<strong>${msg.name}:</strong> ${msg.message}`;
        pensamento.append(span);
    }

    //Realiza uma coneção da nossa instancia socket, enviando a mensagem para o servidor que o usuario foi conectado. 
    socket.on('connect', () => {
        socket.send('Usuário conectado ao socket!')
    });


    //Esta selecionando o primeiro form e manipulando o evento de submit através de uma callback(passando uma função como argumento).
    document.querySelector("form").addEventListener("submit", function(event) {
        event.preventDefault(); //Impede que o evento siga seu fluxo normal, refresh.
        
        //Manda uma mensagem para o Backend, no qual sera recebida pela função sendMessage, contendo um objeto com as chaves nome e message.
        socket.emit('sendMessage', {name: event.target[0].value, message: event.target[1].value})

        //Apos o envio os campos devem ser setados para vázio.
        event.target[0].value = "";
        event.target[1].value = "";
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

likeButton.addEventListener('click', function() {
    toggleIcon(this, 'bi-heart', 'bi-heart-fill');
});

shareButton.addEventListener('click', function() {
    toggleIcon(this, 'bi-share', 'bi-share-fill');
});