const form = document.querySelector('.custom-validation');
// Ocultar el error de longitud mínima al cargar la página
document.getElementById("error_nombre_min").style.display = "none";
document.getElementById("error_nombre_max").style.display = "none";
document.getElementById("error_apellido_min").style.display = "none";
document.getElementById("error_apellido_max").style.display = "none";
document.getElementById("error_fono").style.display = "none";
document.getElementById("error_nacimiento").style.display = "none";
document.getElementById("error_fecha").style.display = "none";
document.getElementById("error_comuna").style.display = "none";
document.getElementById("error_email").style.display = "none";
document.getElementById("error_checkbox").style.display = "none";

const phoneInput = document.querySelector('#idFono');
const iti = window.intlTelInput(phoneInput, {
    utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js',
    initialCountry: 'cl'
});

phoneInput.addEventListener('input', (e) => {
    const value = e.target.value.replace(/\D+/g, '');
    let formattedValue = '';

    // Verifica si el código de país seleccionado es Chile
    if (iti.getSelectedCountryData().iso2 === 'cl') {
        // Aplica el formato de número de teléfono específico para Chile
        if (value.startsWith('9')) {
            formattedValue = formatTelefono9(value);
        } else if (value.startsWith('2')) {
            formattedValue = formatTelefono2(value);
        } else {
            formattedValue = formatTelefono9(value);
        }

        // Limita a 9 dígitos solo para Chile
        if (value.length >= 9) {
            formattedValue = formattedValue.substring(0, 11);

        }


    } else {
        // Aplica el formato de número de teléfono por defecto
        iti.setNumber(value);
        formattedValue = iti.getNumber();

        if (value.length >= 12) {
            formattedValue = formattedValue.substring(0, 17);
        }
    }
    e.target.value = formattedValue;
});

function formatTelefono9(value) {
    if (value.length <= 1) {
        return value;
    } else if (value.length <= 5) {
        return value.replace(/(\d{1})(\d{1,4})/, '$1 $2');
    } else {
        return value.replace(/(\d{1})(\d{4})(\d{1,4})/, '$1 $2 $3');
    }
}

function formatTelefono2(value) {
    if (value.length <= 1) {
        return value;
    } else if (value.length <= 4) {
        return value.replace(/(\d{1})(\d{1,3})/, '$1 $2');
    } else if (value.length <= 7) {
        return value.replace(/(\d{1})(\d{4})(\d{1,2})/, '$1 $2 $3');
    } else {
        return value.replace(/(\d{1})(\d{2})(\d{3})(\d{1,2})/, '$1 $2-$3-$4');
    }
}

// Agregar un listener de eventos al elemento con id "idNombre"
// para que se ejecute la función "validarNombre" cuando el elemento pierda el foco
document.getElementById("idNombre").addEventListener("blur", function () {
    let nombre = document.getElementById("idNombre").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarNombre(nombre);
});
document.getElementById("idApellido").addEventListener("blur", function () {
    let apellido = document.getElementById("idApellido").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarApellido(apellido);
});
document.getElementById("idFono").addEventListener("blur", function () {
    let fono = document.getElementById("idFono").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarFono(fono);

    const prefijoInput = document.querySelector('#prefijo-hidden');
    const prefijoSelect = document.querySelector('.iti');
    const prefijoElement = prefijoSelect.querySelector('[aria-selected="true"]');

    let prefijo = '+'; // Variable para almacenar el prefijo seleccionado

    if (prefijoElement) {
        prefijo += prefijoElement.getAttribute('data-dial-code'); // Obtiene el valor de data-dial-code
    }

    prefijoInput.value = prefijo;
});
document.getElementById("email").addEventListener("blur", function () {
    let email = document.getElementById("email").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarEmail(email);
});
document.getElementById("comuna-select").addEventListener("blur", function () {
    let comuna = document.getElementById("comuna-select").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarComuna(comuna);
});
document.getElementById("idFecha_nac").addEventListener("blur", function () {
    // Obtener el campo de fecha de nacimiento
    let fecha_nac = document.getElementById("idFecha_nac").value;
    // Llamar a la función "validarNombre" con el valor del nombre como argumento
    validarFechaNac(fecha_nac);
});

form.addEventListener('submit', (e) => {
    let isValid = false; // Inicialmente asumimos que el formulario no es válido

    if (validarNombre(document.getElementById("idNombre").value) &&
        validarApellido(document.getElementById("idApellido").value) &&
        validarFono(document.getElementById("idFono").value) &&
        validarFechaNac(document.getElementById("idFecha_nac").value) &&
        validarComuna(document.getElementById("comuna-select").value) &&
        validarEmail(document.getElementById("email").value) &&
        document.getElementById("gridCheck").checked) {
        
        // Si todas las validaciones son exitosas y el checkbox está marcado, el formulario es válido
        isValid = true;
    } else {
        // Si hay algún error de validación o el checkbox no está marcado, el formulario no es válido
        document.getElementById("error_checkbox").style.display = "inline";
    }

    // Previene el envío del formulario si no es válido
    if (!isValid) {
        e.preventDefault();
    }
});

// Funciones de validación específicas para cada campo del formulario
function validarNombre() {
    const nombre = document.getElementById("idNombre").value.trim();
    const errorMin = document.getElementById("error_nombre_min");
    const errorMax = document.getElementById("error_nombre_max");
    const inputNombre = document.getElementById("idNombre");

    if (nombre.length < 3) {
        errorMin.style.display = "inline";
        errorMax.style.display = "none";
        inputNombre.classList.add("is-invalid");
        return false;
    } else if (nombre.length > 20) {
        errorMin.style.display = "none";
        errorMax.style.display = "inline";
        inputNombre.classList.add("is-invalid");
        return false;
    } else {
        errorMin.style.display = "none";
        errorMax.style.display = "none";
        inputNombre.classList.remove("is-invalid");
        inputNombre.classList.add("is-valid");
        return true;
    }
}

function validarApellido() {
    const apellido = document.getElementById("idApellido").value.trim();
    const errorMin = document.getElementById("error_apellido_min");
    const errorMax = document.getElementById("error_apellido_max");
    const inputApellido = document.getElementById("idApellido");

    if (apellido.length < 3) {
        errorMin.style.display = "inline";
        errorMax.style.display = "none";
        inputApellido.classList.add("is-invalid");
        return false;
    } else if (apellido.length > 20) {
        errorMin.style.display = "none";
        errorMax.style.display = "inline";
        inputApellido.classList.add("is-invalid");
        return false;
    } else {
        errorMin.style.display = "none";
        errorMax.style.display = "none";
        inputApellido.classList.remove("is-invalid");
        inputApellido.classList.add("is-valid");
        return true;
    }
}

function validarFono() {
    const fono = document.getElementById("idFono").value.trim();
    const errorFono = document.getElementById("error_fono");
    const inputFono = document.getElementById("idFono");

    if (fono.length < 3) {
        errorFono.style.display = "inline";
        inputFono.classList.add("is-invalid");
        return false;
    } else {
        errorFono.style.display = "none";
        inputFono.classList.remove("is-invalid");
        inputFono.classList.add("is-valid");
        return true;
    }
}

function validarFechaNac() {
    const fechaNac = document.getElementById("idFecha_nac").value.trim();
    const errorNacimiento = document.getElementById("error_nacimiento");
    const errorFecha = document.getElementById("error_fecha");
    const inputFechaNac = document.getElementById("idFecha_nac");

    if (fechaNac === "") {
        errorNacimiento.style.display = "inline";
        errorFecha.style.display = "none";
        inputFechaNac.classList.add("is-invalid");
        return false;
    } else {
        // Validación de edad aquí si es necesario
        errorNacimiento.style.display = "none";
        errorFecha.style.display = "none";
        inputFechaNac.classList.remove("is-invalid");
        inputFechaNac.classList.add("is-valid");
        return true;
    }
}

function validarEmail() {
    const email = document.getElementById("email").value.trim();
    const errorEmail = document.getElementById("error_email");
    const inputEmail = document.getElementById("email");

    if (email === "" || !email.includes("@")) {
        errorEmail.style.display = "inline";
        inputEmail.classList.add("is-invalid");
        return false;
    } else {
        errorEmail.style.display = "none";
        inputEmail.classList.remove("is-invalid");
        inputEmail.classList.add("is-valid");
        return true;
    }
}

function validarComuna() {
    const comuna = document.getElementById("comuna-select").value.trim();
    const errorComuna = document.getElementById("error_comuna");
    const inputComuna = document.getElementById("comuna-select");

    if (comuna === "") {
        errorComuna.style.display = "inline";
        inputComuna.classList.add("is-invalid");
        return false;
    } else {
        errorComuna.style.display = "none";
        inputComuna.classList.remove("is-invalid");
        inputComuna.classList.add("is-valid");
        return true;
    }
}
