const form = document.querySelector('.custom-validation');
// Ocultar el error de longitud mínima al cargar la página
document.addEventListener("DOMContentLoaded", function () {
    var errorElements = document.querySelectorAll(".text-danger");
    errorElements.forEach(function (element) {
        element.style.display = "none";
    });
});

const otherIdNombre = document.getElementById('otherIdNombre');
const otherIdApellido = document.getElementById('otherIdApellido');
const otherIdFecha_nac = document.getElementById('otherIdFecha_nac');
const otherIdCorreo = document.getElementById('otherIdCorreo');
const otherGenero = document.getElementById('otherGenero-select');
const otherComuna = document.getElementById('otherComuna-select');
const otherIdFono = document.getElementById('otherIdFono');

const other_err_nombre_min = document.getElementById('other_err_nombre_min');
const other_err_nombre_max = document.getElementById('other_err_nombre_max');
const other_err_apellido_min = document.getElementById('other_err_apellido_min');
const other_err_apellido_max = document.getElementById('other_err_apellido_max');
const other_err_fono = document.getElementById('other_err_fono');
const other_err_nacimiento = document.getElementById('other_err_nacimiento');
const other_err_email = document.getElementById('other_err_email');
const other_err_comuna = document.getElementById('other_err_comuna');


if (otherIdNombre) {
    otherIdNombre.addEventListener('blur', function () {
        let nombre = this.value;
        validarNombre(nombre, otherIdNombre, other_err_nombre_min, other_err_nombre_max);
    });
}

if (otherIdApellido) {
    otherIdApellido.addEventListener('blur', function () {
        let apellido = this.value;
        validarApellido(apellido, otherIdApellido, other_err_apellido_min, other_err_apellido_max);
    });
}

if (otherIdFecha_nac) {
    otherIdFecha_nac.addEventListener('blur', function () {
        let fecha_nac = this.value;
        validarFechaNac(fecha_nac, otherIdFecha_nac, other_err_nacimiento);
    });
}

if (otherIdCorreo) {
    otherIdCorreo.addEventListener('blur', function () {
        let email = this.value;
        validarEmail(email, otherIdCorreo, other_err_email);
    });
}

if (otherComuna) {
    otherComuna.addEventListener('blur', function () {
        let comuna = this.value;
        validarComuna(comuna, otherComuna, other_err_comuna);
    });
}

if (otherIdFono) {
    otherIdFono.addEventListener('blur', function () {
        let fono = this.value;
        validarFono(fono, otherIdFono, other_err_fono);
        const prefijoInput = document.querySelector('#otherPrefijo-hidden');
        const prefijoSelect = document.querySelector('.iti');
        const prefijoElement = prefijoSelect.querySelector('[aria-selected="true"]');

        if (prefijoElement) {
            prefijo = prefijoElement.getAttribute('data-dial-code'); // Obtiene el valor de data-dial-code
        }

        prefijo_phone = '+'

        prefijoInput.value = prefijo_phone + prefijo;
    });
}

const idNombre = document.getElementById('idNombre');
const idApellido = document.getElementById('idApellido');
const idFecha_nac = document.getElementById('idFecha_nac');
const idCorreo = document.getElementById('idCorreo');
const comuna_select = document.getElementById('comuna-select');
// Verificar si el elemento idContraseña está presente en el DOM
const passwordElement = document.getElementById("idContraseña");
const passwordConfirmElement = document.getElementById("password_confirm");
const phoneInput = document.querySelector('#idFono');

const error_nombre_min = document.getElementById('error_nombre_min');
const error_nombre_max = document.getElementById('error_nombre_max');
const error_apellido_min = document.getElementById('error_apellido_min');
const error_apellido_max = document.getElementById('error_apellido_max');
const error_fono = document.getElementById('error_fono');
const error_nacimiento = document.getElementById('error_nacimiento');
const error_email = document.getElementById('error_email');
const error_comuna = document.getElementById('error_comuna');
const error_password = document.getElementById('error_password');
const error_confirmacion_password = document.getElementById('error_confirm_password');

if (passwordElement) {

    // Agregar evento blur al campo de contraseña (idContraseña)
    passwordElement.addEventListener("blur", function () {
        let password = this.value;
        // Llamar a la función "validarPassword" con el valor de la contraseña como argumento
        validarPassword(password, passwordElement, error_password);
    });
}

if (passwordConfirmElement) {
    // Agregar evento blur al campo de confirmación de contraseña (password_confirm)
    passwordConfirmElement.addEventListener("blur", function () {
        let confirmacionPassword = this.value;
        validarConfirmacionPassword(confirmacionPassword, passwordConfirmElement, error_confirmacion_password);
    });
}




if (otherIdFono) {
    // Configuración inicial de intlTelInput para otherIdFono
    const itiOther = window.intlTelInput(otherIdFono, {
        utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js',
        initialCountry: 'cl'
    });
}
// Configuración inicial de intlTelInput
const iti = window.intlTelInput(phoneInput, {
    utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js',
    initialCountry: 'cl'
});


// Función para aplicar formato de teléfono
function applyPhoneFormat(inputElement) {
    inputElement.addEventListener('input', (e) => {
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
                if (value.startsWith('9')) {
                formattedValue = formattedValue.substring(0, 11);
                } else if (value.startsWith('2')) {
                formattedValue = formattedValue.substring(0, 12);
                }
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
}

// Llama a la función para aplicar el formato al campo visible inicial
applyPhoneFormat(phoneInput);

// Verifica si existe el campo otherIdFono y aplica el formato si es visible
if (otherIdFono) {
    applyPhoneFormat(otherIdFono);
}

// Funciones para el formato específico de teléfono
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
        return value.replace(/(\d{1})(\d{2})(\d{3})(\d{1,3})/, '$1 $2 $3 $4');
    }
}

// Agregar un listener de eventos al elemento con id "idNombre"
// para que se ejecute la función "validarNombre" cuando el elemento pierda el foco

if (idApellido) {
    idApellido.addEventListener('blur', function () {
        let apellido = this.value;
        validarApellido(apellido, idApellido, error_apellido_min, error_apellido_max);
    });
}

if (idNombre) {
    idNombre.addEventListener('blur', function () {
        let nombre = this.value;

        validarNombre(nombre, idNombre, error_nombre_min, error_nombre_max);
    });
}

if (phoneInput) {
    phoneInput.addEventListener('blur', function () {
        const prefijoInput = document.querySelector('#prefijo-hidden');
        const prefijoSelect = document.querySelector('.iti');
        const prefijoElement = prefijoSelect.querySelector('[aria-selected="true"]');
        const fono_formateado = document.getElementById('formatted_phone_number');

        if (prefijoElement) {
            prefijo = prefijoElement.getAttribute('data-dial-code'); // Obtiene el valor de data-dial-code
        }

        prefijo_phone = '+'
        const phoneNumber = this.value.replace(/\s+/g, ''); // Elimina todos los espacios en blanco del número de teléfono

        const fono = prefijo_phone + prefijo + phoneNumber;
        validarFono(fono, phoneInput, error_fono);

        fono_formateado.value = fono;
    });
}


if (idCorreo) {
    idCorreo.addEventListener("blur", function () {
        let email = this.value;
        // Llamar a la función "validarNombre" con el valor del nombre como argumento
        validarEmail(email, idCorreo, error_email);
    });
}

if (idFecha_nac) {
    idFecha_nac.addEventListener("blur", function () {
        let fecha_nac = this.value;
        const error_nacimiento = document.getElementById('error_nacimiento');
        validarFechaNac(fecha_nac, idFecha_nac, error_nacimiento);
    });
}

if (comuna_select) {
    comuna_select.addEventListener('blur', function () {
        let comuna = this.value;
        validarComuna(comuna, comuna_select, error_comuna);
    });
}


// Función para validar el formulario
function validarFormulario(event) {
    event.preventDefault(); // Prevent form submission

    let isValid = true;

    
    if (!(validarNombre(idNombre.value, idNombre, error_nombre_min, error_nombre_max) &&
        validarApellido(idApellido.value, idApellido, error_apellido_min, error_apellido_max) &&
        validarFono(phoneInput.value, phoneInput, error_fono) &&
        validarFechaNac(idFecha_nac.value, idFecha_nac, error_nacimiento) &&
        validarComuna(comuna_select.value, comuna_select, error_comuna) &&
        validarEmail(idCorreo.value, idCorreo, error_email) &&
        document.getElementById("gridCheck").checked)) {

        // Agregar validación del checkbox
        if (!document.getElementById("gridCheck").checked) {
            document.getElementById("error_checkbox").style.display = "inline";
        }

        isValid = false;
    }


}

// Funciones de validación específicas para cada campo del formulario
function validarNombre(nombre, inputNombre, errorMin, errorMax) {
    if (nombre.trim().length < 3) {
        errorMin.style.display = "inline";
        errorMax.style.display = "none";
        inputNombre.classList.add("is-invalid");
        return false;
    } else if (nombre.trim().length > 20) {
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

function validarApellido(apellido, inputApellido, errorMin, errorMax) {

    if (apellido.trim().length < 3) {
        errorMin.style.display = "inline";
        errorMax.style.display = "none";
        inputApellido.classList.add("is-invalid");
        return false;
    } else if (apellido.trim().length > 20) {
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

function validarFono(fono, inputFono, errorFono) {
    const PHONE_REGEX = /^(\+56[92]\d{8}|\+(?!56)\d{1,3}\d{9,15})$/;

    if (!PHONE_REGEX.test(fono.trim())) {
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

function validarFechaNac(fechaNac, inputFechaNac, errorNacimiento) {

    if (fechaNac.trim() === "") {
        errorNacimiento.style.display = "inline";
        inputFechaNac.classList.add("is-invalid");
        return false;
    } else {
        // Validación de edad aquí si es necesario
        errorNacimiento.style.display = "none";
        inputFechaNac.classList.remove("is-invalid");
        inputFechaNac.classList.add("is-valid");
        return true;
    }
}

function validarEmail(email, inputEmail, errorEmail) {

    if (email.trim() === "" || !email.trim().includes("@")) {
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

function validarComuna(comuna, inputComuna, errorComuna) {

    if (comuna.trim() === "") {
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

function validarPassword(password, inputPassword, errorPassword) {

    if (password.length === 0 || password.length < 8 || password.length > 16) {
        if (password.trim().length === 0) {
            errorPassword.style.display = "none";
            inputPassword.classList.remove("is-invalid");
            inputPassword.classList.remove("is-valid");
            return true; // Skip validation if the password is empty with spaces
        } else {
            errorPassword.style.display = "inline";
            inputPassword.classList.add("is-invalid");
            inputPassword.classList.remove("is-valid");
            return false;
        }
    } else if (!/\d/.test(password)) {
        errorPassword.style.display = "inline";
        inputPassword.classList.add("is-invalid");
        return false;
    } else if (!/[a-z]/.test(password) || !/[A-Z]/.test(password)) {
        errorPassword.style.display = "inline";
        inputPassword.classList.add("is-invalid");
        return false;
    } else if (/[^a-zA-Z0-9]/.test(password)) {
        errorPassword.style.display = "inline";
        inputPassword.classList.add("is-invalid");
        return false;
    } else {
        errorPassword.style.display = "none";
        inputPassword.classList.remove("is-invalid");
        inputPassword.classList.add("is-valid");
        return true;
    }
}

function validarConfirmacionPassword(confirmacionPassword, inputConfirmacionPassword, errorConfirmacionPassword) {
    const password = passwordElement.value.trim();

    if (password !== confirmacionPassword) {
        errorConfirmacionPassword.style.display = "inline";
        inputConfirmacionPassword.classList.add("is-invalid");
        return false;
    } else {
        errorConfirmacionPassword.style.display = "none";
        inputConfirmacionPassword.classList.remove("is-invalid");
        inputConfirmacionPassword.classList.add("is-valid");
        return true;
    }
}
