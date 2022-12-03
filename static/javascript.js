
function validarFormulario(){
    
    var directorio = document.getElementById("directorio")
    var nombreDirectorio = directorio.files[0].webkitRelativePath
    // TODO: Check si no es directorio vacío
    
    // Modificamos el campo oculto para añadir el nombre del directorio
    document.getElementById("oculto").value = nombreDirectorio
    return true
}  


