/* dashboard page only script */


/* show the new listing modal */
function openModal() {
  var overlay = document.querySelector(".modal-overlay");
  if (overlay) overlay.classList.add("is-open");
}


/* hide the new listing modal */
function closeModal() {
  var overlay = document.querySelector(".modal-overlay");
  if (overlay) overlay.classList.remove("is-open");
}


/* show or hide the edit form for a specific listing row */
function toggleEdit(productId) {
  var form = document.querySelector("[data-edit-form=" + productId + "]");
  if (!form) return;
  form.classList.toggle("is-open");
}


document.addEventListener("DOMContentLoaded", function () {

  /* wire up the new listing button */
  var openBtn = document.querySelector("[data-open-modal]");
  if (openBtn) openBtn.addEventListener("click", openModal);

  /* wire up the close button inside the modal */
  var closeBtn = document.querySelector(".modal-close");
  if (closeBtn) closeBtn.addEventListener("click", closeModal);

  /* clicking the dark background behind the modal also closes it */
  var overlay = document.querySelector(".modal-overlay");
  if (overlay) {
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeModal();
    });
  }

  /* wire up every edit button in the listings table */
  var editBtns = document.querySelectorAll("[data-edit-btn]");
  editBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      toggleEdit(btn.dataset.editBtn);
    });
  });

  /* ask for confirmation before deleting a listing */
  var deleteBtns = document.querySelectorAll("[data-delete-listing]");
  deleteBtns.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!confirm("Delete this listing? This cannot be undone.")) {
        e.preventDefault();
      }
    });
  });

  /* ask for confirmation before deleting a user account */
  var deleteUserBtns = document.querySelectorAll("[data-delete-user]");
  deleteUserBtns.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      if (!confirm("Delete this user account? This cannot be undone.")) {
        e.preventDefault();
      }
    });
  });

});
