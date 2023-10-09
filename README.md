# Requisitos mínimos
**Memoria RAM:** 16GB

**Espacio de almacenamiento:** 40GB 



# Requisitos recomendados

**Memoria RAM:** 32GB

**Espacio de almacenamiento:** 40GB

**GPU**: Mínimo 5GB de memoria

# Instalar Anaconda

1. Comprobar si Anaconda está instalado en el sistema. Para ello, escribir "Anaconda" en la barra de búsqueda. Si aparecen las aplicaciones "Anaconda Prompt" y "Anaconda Navigator", se puede pasar a la siguiente sección.

2. Acceder a la web oficial
https://www.anaconda.com/download

3. Descargar el instalador asociado al sistema operativo (Windows, Linux o MacOS)

4. Abrir el archivo descargado y seguir las instrucciones de instalación.
    
    - Aceptar las condiciones de uso.
    - Install for: "Just Me".
    - Escoger el directorio donde se instalará. 
    NOTA: es importante que no contenga espacios en blanco.
    - No es necesario añadir la ruta de Anaconda al PATH o registrarlo como Python por defecto.
    - Esperar a que finalice la instalación.
    Verificar que se puede acceder a "Anaconda Navigator" y "Anaconda Prompt".



# Descargar la aplicación
1. Descargar el repositorio como .zip.
2. Colocar la aplicación en el directorio que se desee.

# Importar el entorno de trabajo
1. Dentro del directorio de la aplicación, localizar el archivo "EntornoAnaconda.yaml", dentro de la carpeta "EntornoTrabajo".
2. Conseguir la ubicación del archivo. Deberá seguir el esquema **Ruta_a_la_aplicacion/EntornoTrabajo/EntornoAnaconda.yaml**
3. Abrir la aplicación "Anaconda Prompt".
4. Instalar el entorno de trabajo escribiendo el siguiente comando:
`conda env create -f "Ruta_a_entorno"`
5. Ejecutar el comando `conda env list`
6. Verificar que el entorno "EntornoAdenaV1" aparece en la lista de entornos

# Iniciar la aplicación
1. Abrir la aplicación "Anaconda Prompt".
2. Ejecutar el comando `conda activate EntornoAdenaV1` para empezar a trabajar con el entorno importado.
3. Ejecutar el comando `cd Ruta_a_la_aplicacion`, siendo "Ruta_a_la_aplicacion" la ruta al directorio donde se ha instalado la aplicación.
4. Ejecutar el comando `python app.py`
5. Copiar la dirección de la aplicación que aparece en la consola de comandos. Deberá tener el formato "http://RUTA"
6. Abrir un navegador web como Firefox o Chrome.
7. Pegar la dirección en la barra de búsqueda y pulsar el botón enter

# Usar la aplicación

Ver el archivo "Manual_de_usuario.pdf"

