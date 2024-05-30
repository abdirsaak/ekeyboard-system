document.addEventListener('DOMContentLoaded', () => {
    // Handle quantity increase and decrease
    let quantity = 0;
    const quantityElement = document.getElementById('quantity');
    const quantityInput = document.getElementById('quantity-input');

    document.getElementById('increase-quantity').addEventListener('click', () => {
        quantity++;
        quantityElement.value = quantity;
        quantityInput.value = quantity; // Update the hidden input value
    });

    document.getElementById('decrease-quantity').addEventListener('click', () => {
        if (quantity > 0) {
            quantity--;
            quantityElement.value = quantity;
            quantityInput.value = quantity; // Update the hidden input value
        }
    });
});

setTimeout(function() {
    let flashMessage = document.getElementById("flash-message-2");
    if (flashMessage) {
        flashMessage.style.display = "none";
    }
  }, 3000);