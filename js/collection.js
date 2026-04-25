/* products for collection page */
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

/* show products on the page */
function showProducts(list) {
  const grid = document.querySelector("[data-product-grid]");

  if (!grid) return;

  grid.innerHTML = "";

  list.forEach(function (product) {
    grid.innerHTML += `
      <article class="catalog-card">
        <a href="item.html?id=${product.id}" class="catalog-image ${product.color}">
          <span>${product.name}</span>
          <p>${product.type}</p>
        </a>

        <div class="catalog-copy">
          <div class="catalog-meta">${product.status}</div>

          <h3>
            <a href="item.html?id=${product.id}">${product.name}</a>
          </h3>

          <p>${product.description}</p>

          <div class="catalog-row">
            <span>${showPrice(product.price)}</span>
            <span>${product.type}</span>
          </div>
        </div>
      </article>
    `;
  });
}

/* filter products */
function filterProducts() {
  const search = document.querySelector("[data-search]");
  const type = document.querySelector("[data-type]");
  const status = document.querySelector("[data-status]");

  const searchText = search ? search.value.toLowerCase() : "";
  const selectedType = type ? type.value : "all";
  const selectedStatus = status ? status.value : "all";

  const filtered = products.filter(function (product) {
    const nameMatch = product.name.toLowerCase().includes(searchText);
    const typeMatch = selectedType === "all" || product.type === selectedType;
    const statusMatch = selectedStatus === "all" || product.status === selectedStatus;

    return nameMatch && typeMatch && statusMatch;
  });

  showProducts(filtered);
}

/* collection page setup */
document.addEventListener("DOMContentLoaded", function () {
  const search = document.querySelector("[data-search]");
  const type = document.querySelector("[data-type]");
  const status = document.querySelector("[data-status]");

  showProducts(products);

  if (search) search.addEventListener("input", filterProducts);
  if (type) type.addEventListener("change", filterProducts);
  if (status) status.addEventListener("change", filterProducts);
});