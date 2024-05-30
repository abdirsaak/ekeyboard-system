const productsPerPage = 8;
let currentPage = 1;

const productCards = document.querySelectorAll('.product-card');
const prevPageButton = document.getElementById('prev-page');
const nextPageButton = document.getElementById('next-page');

function displayProducts(page) {
    const start = (page - 1) * productsPerPage;
    const end = start + productsPerPage;

    productCards.forEach((card, index) => {
        if (index >= start && index < end) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });

    prevPageButton.disabled = page === 1;
    nextPageButton.disabled = end >= productCards.length;
}

prevPageButton.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        displayProducts(currentPage);
    }
});

nextPageButton.addEventListener('click', () => {
    if ((currentPage * productsPerPage) < productCards.length) {
        currentPage++;
        displayProducts(currentPage);
    }
});

// Initial display
displayProducts(currentPage);

// Add click event to navigate to product detail page
productCards.forEach(card => {
    card.addEventListener('click', () => {
        const productId = card.getAttribute('data-product-id');
        window.location.href = `/product/${productId}`;
    });
});