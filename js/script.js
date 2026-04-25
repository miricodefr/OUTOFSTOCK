// OUTOFSTOCK™ interactions
// Kept simple on purpose so you can move this into Django later.

document.addEventListener("DOMContentLoaded", function () {
  setupCursorGlow();
  setupSaleItems();
  setupTicker();
  setupColorDots();
  setupParallaxShape();
});

function setupCursorGlow() {
  const glow = document.getElementById("cursorGlow");

  if (!glow) return;

  document.addEventListener("mousemove", function (event) {
    glow.style.left = event.clientX + "px";
    glow.style.top = event.clientY + "px";
    glow.style.opacity = "1";
  });

  document.addEventListener("mouseleave", function () {
    glow.style.opacity = "0";
  });
}

function setupSaleItems() {
  const items = document.querySelectorAll(".sale-item");

  items.forEach(function (item) {
    item.addEventListener("mouseenter", function () {
      item.classList.add("is-hovered");
    });

    item.addEventListener("mouseleave", function () {
      item.classList.remove("is-hovered");
    });
  });
}

function setupTicker() {
  const track = document.getElementById("tickerTrack");

  if (!track) return;

  if (!track.dataset.cloned) {
    track.innerHTML += track.innerHTML;
    track.dataset.cloned = "true";
  }
}

function setupColorDots() {
  const dots = document.querySelectorAll(".dot");
  const body = document.body;

  if (!dots.length) return;

  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      const selectedTheme = dot.getAttribute("data-theme");

      body.classList.remove("theme-dark", "theme-orange", "theme-light");
      body.classList.add("theme-" + selectedTheme);

      dots.forEach(function (currentDot) {
        currentDot.classList.remove("is-active");
      });

      dot.classList.add("is-active");
    });
  });
}

function setupParallaxShape() {
  const shape = document.querySelector(".floating-shape");

  if (!shape) return;

  let mouseX = 0;
  let mouseY = 0;
  let scrollY = 0;

  document.addEventListener("mousemove", function (event) {
    mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
    applyTransform();
  });

  window.addEventListener("scroll", function () {
    scrollY = window.scrollY;
    applyTransform();
  });

  function applyTransform() {
    shape.style.transform =
      "translateY(" + (scrollY * 0.08) + "px) " +
      "rotateX(" + (mouseY * 8) + "deg) " +
      "rotateZ(" + (16 + mouseX * 8 + scrollY * 0.01) + "deg)";
  }
}
