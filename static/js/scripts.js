document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    form.addEventListener('submit', function () {
        form.querySelector('button').innerText = 'Downloading...';
    });
});
