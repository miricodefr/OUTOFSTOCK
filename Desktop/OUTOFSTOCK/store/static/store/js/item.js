/* products used for item page */
const products = [
  {
    id: "starter-store",
    name: "Starter Store",
    price: 45,
    type: "Website",
    status: "Almost Done",
    color: "placeholder-one",
    description: "Small shop idea with basic product pages.",
  },
  {
    id: "study-tracker",
    name: "Study Tracker",
    price: 30,
    type: "App",
    status: "Half Done",
    color: "placeholder-two",
    description: "Student app for tasks, deadlines, and study time.",
  },
  {
    id: "portfolio-kit",
    name: "Portfolio Kit",
    price: 25,
    type: "Website",
    status: "Early Build",
    color: "placeholder-three",
    description: "Personal portfolio layout with project cards.",
  },
  {
    id: "booking-dashboard",
    name: "Booking Dashboard",
    price: 55,
    type: "Dashboard",
    status: "Almost Done",
    color: "placeholder-four",
    description: "Simple dashboard for bookings and basic stats.",
  },
];

/* get item from url */
function getCurrentProduct() {
  const url = new URLSearchParams(window.location.search);
  const id = url.get("id");

  let selectedProduct = products[0];

  products.forEach(function (product) {
    if (product.id === id) {
      selectedProduct = product;
    }
  });

  return selectedProduct;
}

/* show item info */
function showProduct() {
  const product = getCurrentProduct();

  const image = document.querySelector("[data-item-image]");
  const title = document.querySelector("[data-item-title]");
  const price = document.querySelector("[data-item-price]");
  const description = document.querySelector("[data-item-description]");
  const type = document.querySelector("[data-item-type]");
  const status = document.querySelector("[data-item-status]");

  if (image) {
    image.className = "item-visual " + product.color;
    image.innerHTML = "<span>" + product.name + "</span><p>" + product.type + "</p>";
  }

  if (title) title.textContent = product.name;
  if (price) price.textContent = showPrice(product.price);
  if (description) description.textContent = product.description;
  if (type) type.textContent = product.type;
  if (status) status.textContent = product.status;
}

/* add item to cart */
function setupAddButton() {
  const button = document.querySelector("[data-add-to-cart]");

  if (!button) return;

  button.addEventListener("click", function () {
    const product = getCurrentProduct();

    addToCart(product);
    alert("Item added to cart");
  });
}

/* item page setup */
document.addEventListener("DOMContentLoaded", function () {
  showProduct();
  setupAddButton();
});