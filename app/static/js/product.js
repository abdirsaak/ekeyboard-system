

// Toggle navbar visibility
const btn_click = document.querySelector('.btn_click');
const navBar = document.querySelector('#navBar');

btn_click.addEventListener("click", function() {
  navBar.classList.toggle('hidden');
});

// Hide flash message after 3 seconds
setTimeout(function() {
  let flashMessage = document.getElementById("flash-message");
  if (flashMessage) {
      flashMessage.style.display = "none";
  }
}, 3000);

// update category
document.querySelectorAll('.update_btn').forEach(button => {
  button.addEventListener('click', function(event) {
      const categoryId = this.getAttribute('data-id');
      const categoryName = this.getAttribute('data-name');

      // Hide any currently visible update section
      document.querySelectorAll('.update_data').forEach(section => {
          section.classList.add('hidden');
      });

      // Update the values in the update section
      document.getElementById('update-category-id').value = categoryId;
      document.getElementById('update-category-name').value = categoryName;

      // Show the update section
      const updateSection = document.getElementById('updateSection');
      updateSection.classList.remove('hidden');

      // Prevent the click event from bubbling up to the document
      event.stopPropagation();
  });
});

// Hide the update section when clicking outside of it
// document.addEventListener('click', function(event) {
//   const updateSection = document.getElementById('updateSection');
//   if (!updateSection.contains(event.target)) {
//       updateSection.classList.add('hidden');
//   }
// });



// ........... update producr

let close_btn = document.querySelector('.close_btn')
close_btn.addEventListener('click', hideUpdateModal)

function showUpdateModal(product) {


  document.getElementById('updateProductId').value = product[0];
  document.getElementById('updateProductName').value = product[1];
  document.getElementById('updateProductPrice').value = product[2];
  document.getElementById('update_product_selling').value = product[3];
  document.getElementById('updateProductDescription1').value = product[6];
  document.getElementById('updateProductDescription2').value = product[7];
  document.getElementById('updateProductCategory').value = product[8];
  document.getElementById('updateProductInventory').value = product[9];
  let product_id =   document.getElementById('updateProductId').value = product[0];
  console.log("product id", product_id)
  // Update the image previews
  document.getElementById('preview1').src = `{{ url_for('static', filename='product_image/') }}${product[4]}`;
  document.getElementById('preview2').src = `{{ url_for('static', filename='product_image/') }}${product[5]}`;

  document.getElementById('updateModal').classList.remove('hidden');
}

function hideUpdateModal() {
  document.getElementById('updateModal').classList.add('hidden');
}

function previewFile(input) {
  const file = input.files[0];
  const preview = document.getElementById('preview1');
  const reader = new FileReader();

  reader.addEventListener("load", function () {
      preview.src = reader.result;
  }, false);

  if (file) {
      reader.readAsDataURL(file);
  }
}

function previewFile_image(input) {
  const file = input.files[0];
  const preview = document.getElementById('preview2');
  const reader = new FileReader();

  reader.addEventListener("load", function () {
      preview.src = reader.result;
  }, false);

  if (file) {
      reader.readAsDataURL(file);
  }
}
