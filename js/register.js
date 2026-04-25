/* register form check */
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("[data-register-form]");

  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.querySelector("[data-register-name]").value;
    const email = document.querySelector("[data-register-email]").value;
    const password = document.querySelector("[data-register-password]").value;

    if (name === "" || email === "" || password === "") {
      alert("Please fill in all fields");
      return;
    }

    const user = {
      name: name,
      email: email,
    };

    localStorage.setItem(userKey, JSON.stringify(user));

    alert("Account created");
    window.location.href = "dashboard.html";
  });
});