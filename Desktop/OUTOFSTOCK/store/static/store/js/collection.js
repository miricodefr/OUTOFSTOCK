/* collection page only script */


/* hide cards instantly as the user types in the search box */
function filterCards() {
  var input = document.querySelector("[data-search]");
  if (!input) return;

  var query = input.value.toLowerCase().trim();
  var cards = document.querySelectorAll(".catalog-card");

  cards.forEach(function (card) {
    var text = card.textContent.toLowerCase();
    /* show the card if its text contains the query otherwise hide it */
    card.style.display = text.includes(query) ? "" : "none";
  });
}


document.addEventListener("DOMContentLoaded", function () {
  var search = document.querySelector("[data-search]");
  if (search) {
    search.addEventListener("input", filterCards);
  }
});
