/* register page only script */


/* validate all fields before the form reaches Django */
document.addEventListener("DOMContentLoaded", function () {

  var form = document.querySelector(".auth-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    var username = document.querySelector("[name='username']");
    var email    = document.querySelector("[name='email']");
    var password = document.querySelector("[name='password']");

    /* stop if any field is empty */
    if (!username.value.trim() || !email.value.trim() || !password.value.trim()) {
      e.preventDefault();
      alert("All fields are required.");
      return;
    }

    /* very basic email check just looks for an @ sign */
    if (!email.value.includes("@")) {
      e.preventDefault();
      alert("Please enter a valid email address.");
      return;
    }

    /* password must be at least 6 characters long */
    if (password.value.length < 6) {
      e.preventDefault();
      alert("Password must be at least 6 characters long.");
    }
  });

});
