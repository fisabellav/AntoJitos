// Cargar el carrito desde el almacenamiento local al cargar la página

import {addToCart } from './carrito.js';
let listProductHTML = document.querySelector('.all-products');



listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('deseos')) {
        let productElement = positionClick.closest('.product');
        let productId = productElement.dataset.id;
        let productName = productElement.querySelector('.product-title').textContent;
        let productPrice = parseFloat(productElement.querySelector('#product-price').textContent);
        let productImage = productElement.querySelector('img').src;

        let productData = {
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
        };
        console.log(productPrice)
        addToCart(productData);
    }
});



