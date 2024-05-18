function verFile(fileName) {
    fetch(`/file/${fileName}`)
        .then(response => response.text()) 
        .then(content => {
            const p = document.getElementById("contenido");
            p.innerText = content; 
        })
}