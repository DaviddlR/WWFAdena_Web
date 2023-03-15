// Comienza la ejecución a partir de los datos introducidos por el usuario
document.addEventListener('readystatechange', event => { 

    if (event.target.readyState === "complete") {
        // Obtenemos el bloque de texto para escribir mensajes
        var mensajeClustering = document.getElementById("mensajeTareaClustering")
        var mensajeClasificacion = document.getElementById("mensajeTareaClasificacion")

        // Barras de progreso
        var barraClustering = document.getElementById("progressbarClustering")
        var barraClasificacion = document.getElementById("progressbarClasificacion")

        console.log("--EmpezarEjecucion")

        // Enviamos mensajea la direccion /comenzarTarea (ver app.py)

        fetch("/comenzarTarea", {method: "POST"})
        .then(res => res.json())
        .then(res => {
            rutaDestino = res['rutaDestino']
            actualizarTarea(res['url'], mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion, rutaDestino)
        });
    }
    
 });

function actualizarTarea(urlEstado, mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion, rutaDestino){

    // Solicitar info a /estadoTarea
    fetch(urlEstado)
    .then(res => res.json())
    .then(res => {

        // Actualizamos la vista
        mensajeClustering.textContent = res['mensajeClustering']
        mensajeClasificacion.textContent = res['mensajeClasificacion']

        barraClustering.setAttribute("style", "width: " + res["barraClustering"] + "%")
        barraClasificacion.setAttribute("style", "width: " + res["barraClasificacion"] + "%")

        if (res['mensajeClustering'] == "¡Hecho!"){
            document.getElementById("loadingClustering").style.display = "none";
        }

        if (res['mensajeClasificacion'] == "¡Hecho!"){
            document.getElementById("loadingClasificacion").style.display = "none";
        }

        // Comprobamos si la ejecución ha terminado
        if(res['estado'] != 'FINALIZADO'){
            // Volvemos a actualizar a los 500ms
            setTimeout(function(){
                actualizarTarea(urlEstado, mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion, rutaDestino)
            }, 500)
        } else {
            // La ejecución ha finalizado
            document.getElementById("botonVolver").disabled = false;

            // TODO ruta destino
            document.getElementById("listo").innerHTML = "Listo. Puedes encontrar la carpeta de resultados en"
            document.getElementById("pDestino").innerHTML = rutaDestino
        }
    })
}


// Impedir volver atrás

var _hash = "!";
var noBackPlease = function () {
    console.log("noback")
    window.location.href += "#";

    // making sure we have the fruit available for juice....
    // 50 milliseconds for just once do not cost much (^__^)
    window.setTimeout(function () {
        window.location.href += "!";
    }, 50);
};

//Earlier we had setInerval here....
window.onhashchange = function () {
    if (window.location.hash !== _hash) {
        window.location.hash = _hash;
    }
};

window.onload = function () {
    
    noBackPlease();
}
