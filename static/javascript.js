


function validarFormulario(){
    
    var directorio = document.getElementById("directorio")
    var nombreDirectorio = directorio.files[0].webkitRelativePath
    // TODO: Check si no es directorio vacío
    
    // Modificamos el campo oculto para añadir el nombre del directorio
    document.getElementById("oculto").value = nombreDirectorio
    return true
}  


// Comienza la ejecución a partir de los datos introducidos por el usuario
function empezarEjecucion(){

    // Obtenemos el bloque de texto para escribir mensajes
    var mensaje = document.getElementById("mensajeTarea")
    console.log("--EmpezarEjecucion")
    
    // Obtenemos la barra de progreso
    //TODO

    // Enviamos mensajea la direccion /comenzarTarea (ver app.py)

    fetch("/comenzarTarea", {method: "POST"})
    .then(res => res.json())
    .then(res => actualizarTarea(res['url'], mensaje));


    // Se puede hacer con Javascript. Mejor que AJAX
    // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Synchronous_and_Asynchronous_Requests
    // Fetch API.
}


//TODO: Vuelve a ejecutarse solo si la tarea no ha terminado
//TODO: Añadir a nivel general una etiqueta que muestre el estado (EN PROCESO, ERROR, FINALIZADA)
function actualizarTarea(urlEstado, p_mensaje){

    // Solicitar info a /estadoTarea
    fetch(urlEstado)
    .then(res => res.json())
    .then(res => {
        p_mensaje.textContent = res['mensaje']

        if(res['estado'] != 'FINALIZADO'){
            setTimeout(function(){
                actualizarTarea(urlEstado, p_mensaje)
            }, 500)
        }
    })
    



    // Actualizar el p con lo que devuelva
}
