/* cart key used in local storage */
const cartKey = "outofstockCart";

/* user key used in local storage */
const userKey = "outofstockUser";

/* get cart items */
function getCart() {
  const cart = localStorage.getItem(cartKey);

  if (cart) {
    return JSON.parse(cart);
  }

  return [];
}

/* save cart items */
function saveCart(cart) {
  localStorage.setItem(cartKey, JSON.stringify(cart));
}

/* update cart number */
function updateCartCount() {
  const cart = getCart();
  const cartCount = document.querySelector("[data-cart-count]");

  if (!cartCount) return;

  let total = 0;

  cart.forEach(function (item) {
    total += item.quantity;
  });

  cartCount.textContent = total;
}

/* add product to cart */
function addToCart(product) {
  const cart = getCart();
  let found = false;

  cart.forEach(function (item) {
    if (item.id === product.id) {
      item.quantity += 1;
      found = true;
    }
  });

  if (!found) {
    product.quantity = 1;
    cart.push(product);
  }

  saveCart(cart);
  updateCartCount();
}

/* remove product from cart */
function removeFromCart(id) {
  let cart = getCart();

  cart = cart.filter(function (item) {
    return item.id !== id;
  });

  saveCart(cart);
  updateCartCount();
}

/* change product quantity */
function changeQuantity(id, quantity) {
  const cart = getCart();

  cart.forEach(function (item) {
    if (item.id === id) {
      item.quantity = quantity;
    }
  });

  saveCart(cart);
  updateCartCount();
}

/* get total cart price */
function getCartTotal() {
  const cart = getCart();
  let total = 0;

  cart.forEach(function (item) {
    total += item.price * item.quantity;
  });

  return total;
}

/* make price look nicer */
function showPrice(price) {
  return "€" + price.toFixed(2);
}

/* change website theme */
function changeTheme(theme) {
  document.body.classList.remove("theme-light", "theme-orange", "theme-dark");
  document.body.classList.add("theme-" + theme);

  localStorage.setItem("outofstockTheme", theme);
}

/* setup theme buttons */
function setupThemeButtons() {
  const buttons = document.querySelectorAll("[data-theme]");

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      const theme = button.dataset.theme;

      changeTheme(theme);

      buttons.forEach(function (btn) {
        btn.classList.remove("is-active");
      });

      button.classList.add("is-active");
    });
  });
}

/* show current page in nav */
function activeNav() {
  const page = window.location.pathname.split("/").pop();
  const links = document.querySelectorAll(".main-nav a");

  links.forEach(function (link) {
    if (link.getAttribute("href") === page) {
      link.classList.add("active-link");
    }
  });
}

/* create ticker text */
function makeTicker() {
  const ticker = document.querySelector(".ticker-track");

  if (!ticker) return;

  const text =
    "<span>OUTOFSTOCK</span><span class='dot-sep'>●</span>" +
    "<span>UNFINISHED PROJECTS</span><span class='dot-sep'>●</span>" +
    "<span>LIMITED DROPS</span><span class='dot-sep'>●</span>" +
    "<span>NO RESTOCKS</span><span class='dot-sep'>●</span>";

  ticker.innerHTML = text + text;
}

/* mouse glow effect */
function mouseGlow() {
  const glow = document.querySelector(".cursor-glow");

  if (!glow) return;

  window.addEventListener("mousemove", function (event) {
    glow.style.opacity = "1";
    glow.style.left = event.clientX + "px";
    glow.style.top = event.clientY + "px";
  });
}

/* run shared code */
document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("outofstockTheme") || "light";

  changeTheme(savedTheme);
  setupThemeButtons();
  activeNav();
  makeTicker();
  mouseGlow();
  updateCartCount();
});