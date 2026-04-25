/* move hero shape with mouse */
document.addEventListener("DOMContentLoaded", function () {
  const shape = document.querySelector(".floating-shape");

  if (!shape) return;

  window.addEventListener("mousemove", function (event) {
    const x = (event.clientX / window.innerWidth - 0.5) * 18;
    const y = (event.clientY / window.innerHeight - 0.5) * 18;

    shape.style.transform = "rotate(16deg) translate(" + x + "px, " + y + "px)";
  });
});