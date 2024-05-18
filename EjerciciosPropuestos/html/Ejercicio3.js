function crearArchivo() {
    const nombre= document.getElementById("nombre").value;
    const texto=document.getElementById("texto").value;
    const data = {
        name:nombre,
        txt:texto
    };
    fetch('/crear', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    verLista();
}