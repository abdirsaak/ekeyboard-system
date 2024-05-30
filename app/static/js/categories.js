let category_icon = document.querySelector(".category_icon")
let categories = document.querySelector(".categories")



category_icon.addEventListener("click", dispay_categories)

function dispay_categories(){
    categories.classList.toggle("hidden")
}