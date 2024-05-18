function verFile(fileName) {
    fetch(`/file/${fileName}`)
        .then(response => response.text()) 
        .then(data => {
            const div = document.getElementById("div");
            div.innerHTML = data;
        })
}