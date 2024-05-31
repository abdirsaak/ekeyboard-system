document.addEventListener("DOMContentLoaded", () => {
    const cartBtn = document.querySelector('.cart_btn');
    const cartContainer = document.querySelector('.cart_container');
    const closeCartBtn = document.querySelector(".close_cart");
    const totalPriceElement = document.querySelector('.total_price');

    const displayProductCart = () => {
        cartContainer.classList.toggle("hidden");
        updateTotalPrice();  // Update total price when the cart is displayed
    };

    if (cartBtn) {
        cartBtn.addEventListener("click", displayProductCart);
    }

    if (closeCartBtn) {
        closeCartBtn.addEventListener("click", () => {
            cartContainer.classList.add("hidden");
        });
    }

    const updateTotalPrice = () => {
        let total = 0;
        document.querySelectorAll('.item-total').forEach(itemTotal => {
            total += parseFloat(itemTotal.textContent);
        });
        totalPriceElement.textContent = total.toFixed(2);
    };

    document.querySelectorAll('.increment').forEach(button => {
        button.addEventListener('click', () => {
            const cartItem = button.closest('[data-id]');
            const quantityInput = cartItem.querySelector('.quantity');
            const itemTotalElement = cartItem.querySelector('.item-total');
            const price = parseFloat(cartItem.dataset.price);

            let quantity = parseInt(quantityInput.value);
            quantity++;
            quantityInput.value = quantity;
            itemTotalElement.textContent = (price * quantity).toFixed(2);

            updateTotalPrice();
        });
    });

    document.querySelectorAll('.decrement').forEach(button => {
        button.addEventListener('click', () => {
            const cartItem = button.closest('[data-id]');
            const quantityInput = cartItem.querySelector('.quantity');
            const itemTotalElement = cartItem.querySelector('.item-total');
            const price = parseFloat(cartItem.dataset.price);

            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantity--;
                quantityInput.value = quantity;
                itemTotalElement.textContent = (price * quantity).toFixed(2);

                updateTotalPrice();
            }
        });
    });

    updateTotalPrice(); // Initial update of the total price when the page loads
});
