function verLista() {
    fetch(`/files`) 
        .then(response => response.json())
        .then(response => {
            const div = document.getElementById("lista");
            div.innerHTML = ""; 
            response.files.forEach(file => {
                const p = document.createElement("p");
                p.textContent = file;
                div.appendChild(p);
                div.addEventListener("click", ()=> verFile(file));
            });
        })
}
verLista();