/* product detail page only script */


/* let keyboard users click star labels using enter or space key */
function setupStars() {
  var labels = document.querySelectorAll(".star-picker label");
  labels.forEach(function (label) {
    label.setAttribute("tabindex", "0");
    label.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        label.click();
      }
    });
  });
}


document.addEventListener("DOMContentLoaded", function () {
  setupStars();
});
