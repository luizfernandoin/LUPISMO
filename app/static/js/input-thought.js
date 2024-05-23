document.addEventListener('DOMContentLoaded', function () {
    const editableDiv = document.getElementById('thought');
    const charCounter = document.querySelector('.char-counter');
    const placeholderText = 'Digite seu pensamento aqui...';
    const maxChars = 1000;

    // Adiciona o texto placeholder se a div estiver vazia
    if (editableDiv.innerHTML.trim() === '') {
        editableDiv.classList.add('empty');
        editableDiv.setAttribute('data-placeholder', placeholderText);
    }

    // Remove o placeholder quando a div recebe foco
    editableDiv.addEventListener('focus', function () {
        if (editableDiv.classList.contains('empty')) {
            editableDiv.classList.remove('empty');
            editableDiv.innerHTML = '';
        }
    });

    // Adiciona o placeholder se a div perder o foco e estiver vazia
    editableDiv.addEventListener('blur', function () {
        if (editableDiv.innerHTML.trim() === '') {
            editableDiv.classList.add('empty');
            editableDiv.innerHTML = '';
            editableDiv.setAttribute('data-placeholder', placeholderText);
        }
    });

    // Monitora mudanças de conteúdo na div
    editableDiv.addEventListener('input', function () {
        // Atualiza a contagem de caracteres
        updateCharCounter();

        // Verifica e limita o número de caracteres
        const text = editableDiv.innerText;
        if (text.length > maxChars) {
            // Mantém o cursor no final do texto
            const selection = window.getSelection();
            const startPos = selection.getRangeAt(0).startOffset;
            editableDiv.innerText = text.substring(0, maxChars);

            // Restaura a posição do cursor
            if (startPos > maxChars) {
                selection.setPosition(editableDiv.firstChild, maxChars);
            }

            updateCharCounter();
        }
    });

    // Função para atualizar a contagem de caracteres
    function updateCharCounter() {
        const textLength = editableDiv.innerText.length;
        charCounter.textContent = `${textLength} / ${maxChars}`;
    }
});
