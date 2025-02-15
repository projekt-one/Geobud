document.addEventListener("DOMContentLoaded", function () {
    loadProjects();

    document.getElementById("projekt-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(event.target);

        fetch("/zapisz_projekt", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            loadProjects();
        });
    });

    function loadProjects() {
        fetch("/projekty")
        .then(response => response.json())
        .then(projekty => {
            const lista = document.getElementById("projekty-lista");
            lista.innerHTML = "";

            projekty.forEach(projekt => {
                const li = document.createElement("li");
                li.innerHTML = `<b>${projekt.nazwa}</b> - ${projekt.lokalizacja} - <a href="${projekt.projekt_link}" target="_blank">Zobacz projekt</a>`;
                lista.appendChild(li);
            });
        });
    }
});
