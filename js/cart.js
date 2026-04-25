/* show cart items */
function showCart() {
  const cartBox = document.querySelector("[data-cart-items]");
  const totalBox = document.querySelector("[data-cart-total]");
  const cart = getCart();

  if (!cartBox || !totalBox) return;

  cartBox.innerHTML = "";

  if (cart.length === 0) {
    cartBox.innerHTML = "<p>Your cart is empty.</p>";
    totalBox.textContent = showPrice(0);
    return;
  }

  cart.forEach(function (item) {
    cartBox.innerHTML += `
      <div class="cart-item-row">
        <div class="cart-thumb ${item.color}">
          <span>${item.name}</span>
        </div>

        <div>
          <h3>${item.name}</h3>
          <p>${item.type}</p>
          <p>${showPrice(item.price)}</p>
        </div>

        <div>
          <input type="number" min="1" value="${item.quantity}" data-cart-quantity="${item.id}">
          <button data-remove-item="${item.id}">Remove</button>
        </div>
      </div>
    `;
  });

  totalBox.textContent = showPrice(getCartTotal());
}

/* cart buttons */
document.addEventListener("DOMContentLoaded", function () {
  const cartBox = document.querySelector("[data-cart-items]");
  const checkout = document.querySelector("[data-checkout]");

  showCart();

  if (cartBox) {
    cartBox.addEventListener("input", function (event) {
      const input = event.target.closest("[data-cart-quantity]");

      if (!input) return;

      changeQuantity(input.dataset.cartQuantity, Number(input.value));
      showCart();
    });

    cartBox.addEventListener("click", function (event) {
      const button = event.target.closest("[data-remove-item]");

      if (!button) return;

      removeFromCart(button.dataset.removeItem);
      showCart();
    });
  }

  if (checkout) {
    checkout.addEventListener("click", function () {
      if (getCart().length === 0) {
        alert("Your cart is empty");
        return;
      }

      localStorage.removeItem(cartKey);
      updateCartCount();
      showCart();

      alert("Checkout complete");
    });
  }
});