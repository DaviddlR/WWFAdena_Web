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
        .then(res => actualizarTarea(res['url'], mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion));
    }
    
 });



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


//  $(window).on("keypress", function (e){
//     if(e.keycode == "backspace") 
//          e.preventDefault();
// })

//  window.addEventListener("beforeunload", function(event) {
//     console.log("UNLOAD:1");
//     //event.preventDefault();
//     event.returnValue = "AA"; //"Any text"; //true; //false;
//     //return null; //"Any text"; //true; //false;
//   });

// document.addEventListener('visibilitychange', function logData() {
//     if (document.visibilityState === 'hidden') {
//       alert("No te vallas")
//     }
//   });


//TODO: Vuelve a ejecutarse solo si la tarea no ha terminado
//TODO: Añadir a nivel general una etiqueta que muestre el estado (EN PROCESO, ERROR, FINALIZADA)
function actualizarTarea(urlEstado, mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion){

    // Solicitar info a /estadoTarea
    fetch(urlEstado)
    .then(res => res.json())
    .then(res => {
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

        if(res['estado'] != 'FINALIZADO'){
            setTimeout(function(){
                actualizarTarea(urlEstado, mensajeClustering, mensajeClasificacion, barraClustering, barraClasificacion)
            }, 500)
        } else {
            // La ejecución ha finalizado
            document.getElementById("botonVolver").disabled = false;
        }
    })
    



    // Actualizar el p con lo que devuelva
}
