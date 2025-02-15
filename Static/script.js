document.addEventListener("DOMContentLoaded", function () {
    // Pobieranie listy zapisanych projektów
    fetch('/projekty')
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById("projekty");
            data.forEach(projekt => {
                let option = document.createElement("option");
                option.text = projekt.nazwa;
                option.value = projekt.projekt_link;
                select.appendChild(option);
            });
        });

    // Inicjalizacja mapy Leaflet
    var map = L.map('map').setView([52.2298, 21.0122], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Obsługa formularza generowania PDF
    document.getElementById('wniosekForm').addEventListener('submit', function (event) {
        event.preventDefault();
        let formData = new FormData(this);
        fetch('/generate_pdf', {
            method: 'POST',
            body: formData
        })
            .then(response => response.blob())
            .then(blob => {
                let url = window.URL.createObjectURL(blob);
                window.location.assign(url);
            });
    });

    // Pobieranie warunków zabudowy MPZP
    document.getElementById("btnMPZP").addEventListener("click", function () {
        let lokalizacja = document.getElementById("lokalizacja").value;
        fetch(`/mpzp?lokalizacja=${lokalizacja}`)
            .then(response => response.json())
            .then(data => alert("Warunki zabudowy: " + JSON.stringify(data)));
    });

    // Analiza nasłonecznienia
    document.getElementById("btnSlonce").addEventListener("click", function () {
        let lokalizacja = document.getElementById("lokalizacja").value;
        fetch(`/analiza_slonca?lokalizacja=${lokalizacja}`)
            .then(response => response.json())
            .then(data => alert("Optymalne ustawienie: " + JSON.stringify(data)));
    });
});
