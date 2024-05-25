document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('capa');
    const preview = document.getElementById('preview');

    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                preview.src = reader.result;
            };
            reader.readAsDataURL(file);
        }
    });
});
