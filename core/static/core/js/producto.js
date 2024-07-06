import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.product-detail');
document.addEventListener('DOMContentLoaded', function() {

    let cantidadValor = document.getElementById('cantidad-valor');
    let cantidadSeleccionada = document.querySelectorAll('.cantidad');
    let menosCantidad = document.getElementById('menos-cantidad');
    let masCantidad = document.getElementById('mas-cantidad');

    let cantidad = parseInt(cantidadValor.textContent);

    // Iterar sobre cada elemento con la clase '.cantidad'
    cantidadSeleccionada.forEach(elemento => {
        elemento.addEventListener('input', function() {
            if (parseInt(elemento.value) < 1) {
                elemento.value = 1;
            }
        });
    });
    
    
    function actualizarCantidadSeleccionada() {
        cantidadSeleccionada.forEach(elemento => {
            elemento.value = cantidad;
        });
    }

    function actualizarCantidadValor() {
        cantidad = parseInt(cantidadSeleccionada[0].value); // Suponemos que solo tomamos el valor del primer elemento para actualizar el total
        cantidadValor.textContent = cantidad;
    }

    menosCantidad.addEventListener('click', () => {
        if (cantidad > 1) {
            cantidad--;
            cantidadValor.textContent = cantidad;
            actualizarCantidadSeleccionada();
        }
    });

    masCantidad.addEventListener('click', () => {
        cantidad++;
        cantidadValor.textContent = cantidad;
        actualizarCantidadSeleccionada();
    });

    // Escuchar cambios en el primer elemento con la clase '.cantidad'
    cantidadSeleccionada[0].addEventListener('input', () => {
        actualizarCantidadValor();
    });

    actualizarCantidadSeleccionada();
});



listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('deseos')) {
        let productElement = positionClick.closest('.product');
        let cantidadValor = document.getElementById('cantidad-valor');

        if (cantidadValor) {
            let productId = productElement.dataset.id;
            let productName = productElement.querySelector('.product-title').textContent;
            let productQuantity = parseInt(cantidadValor.textContent);
            let productImage = productElement.querySelector('img').src;

            let productData = {
                id: productId,
                name: productName,
                image: productImage,
                quantity: productQuantity
            };

            console.log(productId);
            addToCart(productData);
        } else {
            console.error('Cantidad valor no encontrado en el producto:', productElement);
        }
    }
});