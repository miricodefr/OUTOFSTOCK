/* login page only script */


/* check that both fields are filled before the form submits */
document.addEventListener("DOMContentLoaded", function () {

  var form = document.querySelector(".auth-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    var username = document.querySelector("[name='username']");
    var password = document.querySelector("[name='password']");

    if (!username.value.trim() || !password.value.trim()) {
      e.preventDefault();
      alert("Please fill in both fields.");
    }
  });

});
