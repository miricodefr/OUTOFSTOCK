/* home page only script */


/* make the floating shape drift slightly when the mouse moves */
document.addEventListener("DOMContentLoaded", function () {

  var shape = document.querySelector(".floating-shape");

  if (shape) {
    window.addEventListener("mousemove", function (e) {
      /* figure out how far the mouse is from the center of the screen */
      var x = (e.clientX / window.innerWidth  - 0.5) * 18;
      var y = (e.clientY / window.innerHeight - 0.5) * 18;
      shape.style.transform = "rotate(16deg) translate(" + x + "px, " + y + "px)";
    });
  }

});
