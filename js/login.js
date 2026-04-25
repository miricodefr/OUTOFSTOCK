/* login form check */
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("[data-login-form]");

  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const email = document.querySelector("[data-login-email]").value;
    const password = document.querySelector("[data-login-password]").value;

    if (email === "" || password === "") {
      alert("Please fill in all fields");
      return;
    }

    localStorage.setItem(userKey, email);

    alert("Logged in successfully");
    window.location.href = "dashboard.html";
  });
});