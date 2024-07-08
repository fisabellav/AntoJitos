import { removeFromCart, loadCartFromLocalStorage, changeQuantityCart, listCartHTML} from './carrito.js';


let iconCart = document.querySelector('.icon-cart');


let closeCart = document.querySelector('.close');



iconCart.addEventListener('click', () => {
    const cartTab = document.querySelector('.cartTab');
    cartTab.classList.toggle('showCart');
    document.body.classList.toggle('showCart');
});

closeCart.addEventListener('click', () => {
    const cartTab = document.querySelector('.cartTab');
    cartTab.classList.toggle('showCart');
    document.body.classList.toggle('showCart');
});


listCartHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if (positionClick.classList.contains('minus') || positionClick.classList.contains('plus')) {
        let product_id = positionClick.parentElement.parentElement.dataset.id;
        let type = 'minus';
        if (positionClick.classList.contains('plus')) {
            type = 'plus';
        }
        changeQuantityCart(product_id, type);
    }
    if (positionClick.classList.contains('fa-trash')) {
        let product_id = positionClick.closest('.item').dataset.id;
        removeFromCart(product_id);
    }
})

// Evento para cargar el carrito desde el almacenamiento local cuando se carga la página
window.addEventListener('DOMContentLoaded', () => {
    loadCartFromLocalStorage();
});
