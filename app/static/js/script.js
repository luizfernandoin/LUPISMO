import { socket } from "./socket.js";

var likeButton = document.querySelector('.like-button');
var shareButton = document.querySelector('.share-button');

//Realiza uma coneção da nossa instancia socket, enviando a mensagem para o servidor que o usuario foi conectado. 
socket.on('connect', () => {
    socket.send('Usuário conectado ao socket!')
});


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