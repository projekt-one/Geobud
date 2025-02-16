document.addEventListener("DOMContentLoaded", function () {
    loadProjects();
});

document.getElementById("projekt-form").addEventListener("submit", function(event) {
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
    })
    .catch(error => console.error("Błąd:", error));
});

function loadProjects() {
    fetch("/projekty")
    .then(response => response.json())
    .then(projekty => {
        const lista = document.getElementById("projekty-lista");
        lista.innerHTML = "";
        projekty.forEach(projekt => {
            const div = document.createElement("div");
            div.classList.add("projekt");
            div.innerHTML = `
                <img src="${projekt.obrazek}" alt="Projekt">
                <h3>${projekt.nazwa}</h3>
                <p>${projekt.lokalizacja}</p>
                <a href="${projekt.projekt_link}" target="_blank">Zobacz projekt</a>
            `;
            lista.appendChild(div);
        });
    })
    .catch(error => console.error("Błąd:", error));
}
