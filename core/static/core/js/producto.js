import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.product-detail');
document.addEventListener('DOMContentLoaded', function() {

    let cantidadValor = document.getElementById('cantidad-valor');
    let cantidadSeleccionada = document.getElementById('idCantidad');
    let menosCantidad = document.getElementById('menos-cantidad');
    let masCantidad = document.getElementById('mas-cantidad');

    let cantidad = parseInt(cantidadValor.textContent);

    cantidadSeleccionada.addEventListener('input', function() {
        if (parseInt(cantidadSeleccionada.value) < 1) {
            cantidadSeleccionada.value = 1;
        }
    });
    
    function actualizarCantidadSeleccionada() {
        cantidadSeleccionada.value = cantidad;
    }

    function actualizarCantidadValor() {
        cantidad = parseInt(cantidadSeleccionada.value);
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

    cantidadSeleccionada.addEventListener('input', () => {
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