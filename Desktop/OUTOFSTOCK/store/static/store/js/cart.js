/* cart page only script */


/* ask the user to confirm before removing an item from the cart */
function setupRemoveButtons() {
  var links = document.querySelectorAll("[data-remove-link]");
  links.forEach(function (link) {
    link.addEventListener("click", function (e) {
      var confirmed = confirm("Remove this item from your cart?");
      if (!confirmed) {
        e.preventDefault();
      }
    });
  });
}


document.addEventListener("DOMContentLoaded", function () {
  setupRemoveButtons();
});
