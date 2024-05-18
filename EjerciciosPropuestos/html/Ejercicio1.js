function verLista() {
    fetch(`/files`) 
        .then(response => response.json())
        .then(response => {
            const ul = document.getElementById("lista");
            ul.innerHTML = ""; 
            response.files.forEach(file => {
                const li = document.createElement("li");
                li.textContent = file;
                ul.appendChild(li);
                ul.addEventListener("click", ()=> verFile(file));
            });
        })
}
verLista();