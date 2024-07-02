let iconCartSpan = document.querySelector('.icon-cart span');
let listCartHTML = document.querySelector('.listCart');
let cart = [];
// Función para eliminar producto del carrito
export const removeFromCart = (product_id) => {
    cart = cart.filter(item => item.id !== product_id);
    addCartToHTML();
    saveCartToLocalStorage(); // Guardar carrito en localStorage
}

// Función para guardar el carrito en el almacenamiento local
export const saveCartToLocalStorage = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Función para cargar el carrito desde el almacenamiento local
export const loadCartFromLocalStorage = () => {
    const storedCart = localStorage.getItem('cart');
    if (storedCart) {
        cart = JSON.parse(storedCart);
        addCartToHTML(); // Actualizar la interfaz de usuario con el contenido del carrito cargado
    }
};

export const addToCart = (productData) => {
    let positionThisProductInCart = cart.findIndex((value) => value.id == productData.id);
    if (cart.length <= 0) {
        cart = [{
            id: productData.id,
            name: productData.name,
            image: productData.image,
            quantity: productData.quantity || 1,  // Utiliza productData.quantity si está presente, de lo contrario 1
        }];
    } else if (positionThisProductInCart < 0) {
        cart.push({
            id: productData.id,
            name: productData.name,
            image: productData.image,
            quantity: productData.quantity || 1,  // Utiliza productData.quantity si está presente, de lo contrario 1
        });
    } else {
        if (productData.quantity) {
            cart[positionThisProductInCart].quantity += productData.quantity;
        } else {
            cart[positionThisProductInCart].quantity += 1;
        }
    }
    addCartToHTML();
    saveCartToLocalStorage(); // Guardar el carrito en el almacenamiento local después de actualizarlo
}

export const changeQuantityCart = (product_id, type) => {
    let positionItemInCart = cart.findIndex((value) => value.id == product_id);
    if (positionItemInCart >= 0) {
        let info = cart[positionItemInCart];
        switch (type) {
            case 'plus':
                cart[positionItemInCart].quantity = cart[positionItemInCart].quantity + 1;
                break;

            case 'minus':
                if (cart[positionItemInCart].quantity > 1) {
                    cart[positionItemInCart].quantity = cart[positionItemInCart].quantity - 1;
                }
                break;
        }
        addCartToHTML();
        saveCartToLocalStorage(); // Guardar el carrito en el almacenamiento local después de actualizarlo
    }
}


export const addCartToHTML = () => {
    listCartHTML.innerHTML = '';
    let totalQuantity = 0;
    if (cart.length > 0) {
        cart.forEach(item => {
            totalQuantity = totalQuantity + item.quantity;
            let newItem = document.createElement('div');
            newItem.classList.add('item');
            newItem.dataset.id = item.id;

            newItem.innerHTML = `
        <div class="image">
            <img src="${item.image}">
        </div>
        <div class="name">
            ${item.name}
        </div>
        
        <div class="quantity">
            <span class="minus"><</span>
            <span>${item.quantity}</span>
            <span class="plus">></span>
        </div>
        <div class="remove">
            <i class="fa fa-trash"></i>
        </div>
        `;
            listCartHTML.appendChild(newItem);
        })
    }
    iconCartSpan.innerText = totalQuantity;
}

export { cart, listCartHTML };