// Function to preview the first image
function previewFile() {
    const preview = document.querySelector("#preview");
    const file = document.querySelector("input[type=file]").files[0];
    const reader = new FileReader();
  
    reader.addEventListener("load", function () {
        preview.src = reader.result;
    }, false);
  
    if (file) {
        reader.readAsDataURL(file);
    }
  }
  
  // Function to preview the second image
  function previewFile_image() {
    const preview_image_2 = document.querySelector("#preview_image_2");
    const file2 = document.querySelector("input[type=file]").files[0];
    const reader = new FileReader();
  
    reader.addEventListener("load", function () {
        preview_image_2.src = reader.result;
    }, false);
  
    if (file2) {
        reader.readAsDataURL(file2);
    }
  }