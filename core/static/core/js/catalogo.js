// Almacena la posición de desplazamiento antes de recargar la página
window.addEventListener('beforeunload', function () {
    localStorage.setItem('scrollPosition', window.pageYOffset);
});

// Restaura la posición de desplazamiento después de recargar la página
window.addEventListener('load', function () {
    if (localStorage.getItem('scrollPosition')) {
        window.scrollTo(0, localStorage.getItem('scrollPosition'));
        localStorage.removeItem('scrollPosition');
    }
});

// Ajustar la altura del select según el número de opciones seleccionadas
function ajustarAlturaSelect() {
    const selectElement = document.getElementById('flavor-filter');
    const numOptions = selectElement.options.length; // Obtener el número total de opciones
    selectElement.size = numOptions > 0 ? numOptions : 1; // Ajustar el tamaño del select
}

// Llamar a la función cuando se cargue el contenido inicialmente
document.addEventListener('DOMContentLoaded', function() {
    ajustarAlturaSelect();
});

// Llamar a la función cada vez que cambian las selecciones en el select
document.getElementById('flavor-filter').addEventListener('change', function() {
    ajustarAlturaSelect();
});
