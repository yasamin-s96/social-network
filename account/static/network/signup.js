document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.custom-file-input').forEach(element => {
        element.addEventListener("change", event => {
            if (event.target.files[0]) {
                event.target.parentElement.querySelector('.custom-file-label').innerText = event.target.files[0].name;
            } else {
                if (event.target.id == 'profile') {
                    event.target.parentElement.querySelector('.custom-file-label').innerHTML = `<span style="color: #6c757d;">Choose profile picture<span>`;
                } else if (event.target.id == 'cover') {
                    event.target.parentElement.querySelector('.custom-file-label').innerHTML = `<span style="color: #6c757d;">Choose cover picture<span>`;
                }
            }
        });
    });
});