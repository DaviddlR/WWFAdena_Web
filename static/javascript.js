
function validarFormulario(){
    console.log("Validando formulario...")
    puedeEnviar = false

    if(document.getElementById("directorio").value != "") {
        var directorio = document.getElementById("directorio")
        var nombreDirectorio = directorio.files[0].webkitRelativePath
        // TODO: Check si son imagenes
        
        // Modificamos el campo oculto para añadir el nombre del directorio
        document.getElementById("oculto").value = nombreDirectorio
        puedeEnviar = true
     } else {
        alert("Debes seleccionar el directorio donde se encuentran las imágenes")
     }
    
    return puedeEnviar
    
}  


