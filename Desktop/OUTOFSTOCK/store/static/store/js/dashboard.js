/* show user on dashboard */
function showUser() {
  const savedUser = localStorage.getItem(userKey);
  const nameBox = document.querySelector("[data-user-name]");
  const emailBox = document.querySelector("[data-user-email]");

  if (!nameBox || !emailBox) return;

  if (!savedUser) {
    nameBox.textContent = "Guest";
    emailBox.textContent = "Not logged in";
    return;
  }

  if (savedUser.includes("{")) {
    const user = JSON.parse(savedUser);

    nameBox.textContent = user.name;
    emailBox.textContent = user.email;
  } else {
    nameBox.textContent = "User";
    emailBox.textContent = savedUser;
  }
}

/* show dashboard numbers */
function showStats() {
  const countBox = document.querySelector("[data-dashboard-cart-count]");
  const totalBox = document.querySelector("[data-dashboard-cart-total]");

  if (countBox) countBox.textContent = getCart().length;
  if (totalBox) totalBox.textContent = showPrice(getCartTotal());
}

/* dashboard setup */
document.addEventListener("DOMContentLoaded", function () {
  const logout = document.querySelector("[data-logout]");

  showUser();
  showStats();

  if (logout) {
    logout.addEventListener("click", function () {
      localStorage.removeItem(userKey);

      alert("Logged out");
      window.location.href = "login.html";
    });
  }
});