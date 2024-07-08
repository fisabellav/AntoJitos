import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.product-detail');
document.addEventListener('DOMContentLoaded', function() {

    let cantidadValorInput = document.getElementById('cantidad-valor');
    let cantidadValorLabel = document.getElementById('cantidad-valor-label');
    let menosCantidad = document.getElementById('menos-cantidad');
    let masCantidad = document.getElementById('mas-cantidad');
    let idCantidadInput = document.getElementById('idCantidad');

    let cantidad = parseInt(cantidadValorInput.value);

    function actualizarCantidad() {
        cantidadValorInput.value = cantidad;
        cantidadValorLabel.textContent = cantidad;
        idCantidadInput.value = cantidad
    }

    menosCantidad.addEventListener('click', () => {
        if (cantidad > 1) {
            cantidad--;
            actualizarCantidad();
        }
    });

    masCantidad.addEventListener('click', () => {
        cantidad++;
        actualizarCantidad();
    });

    cantidadValorInput.addEventListener('input', () => {
        cantidad = parseInt(cantidadValorInput.value);
        actualizarCantidad();
    });

    idCantidadInput.addEventListener('input', () => {
        cantidad = parseInt(idCantidadInput.value);
        actualizarCantidad();
    });

    actualizarCantidad();
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
            let productPrice = parseFloat(productElement.querySelector('#product-price').textContent);


            let productData = {
                id: productId,
                name: productName,
                image: productImage,
                quantity: productQuantity,
                price: productPrice
            };

            console.log(productId);
            addToCart(productData);
        } else {
            console.error('Cantidad valor no encontrado en el producto:', productElement);
        }
    }
});