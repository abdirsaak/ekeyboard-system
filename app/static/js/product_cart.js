let cart_btn  =document.querySelector('.cart_btn')
let cart_container = document.querySelector('.cart_container')
let close_cart = document.querySelector(".close_cart")


const display_product_cart = () => {
    cart_container.classList.toggle("hidden")
}


cart_btn.addEventListener("click", display_product_cart)

close_cart.addEventListener("click", () => {
    cart_container.classList.add("hidden")
})
