/* this file runs on every single page of the site */


/* change the color theme of the page */
function changeTheme(theme) {
  /* remove whichever theme class is currently on the body */
  document.body.classList.remove("theme-light", "theme-dark", "theme-orange");
  /* add the new one */
  document.body.classList.add("theme-" + theme);
  /* save the choice so it is remembered on the next visit */
  localStorage.setItem("outofstockTheme", theme);
}


/* connect the three color dot buttons on the home page */
function setupThemeButtons() {
  var buttons = document.querySelectorAll("[data-theme]");
  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      changeTheme(btn.dataset.theme);
      /* remove the active ring from all dots then add it to the clicked one */
      buttons.forEach(function (b) { b.classList.remove("is-active"); });
      btn.classList.add("is-active");
    });
  });
}


/* make the orange glow circle follow the mouse */
function mouseGlow() {
  var glow = document.querySelector(".cursor-glow");
  if (!glow) return;
  window.addEventListener("mousemove", function (e) {
    glow.style.opacity = "1";
    glow.style.left = e.clientX + "px";
    glow.style.top  = e.clientY + "px";
  });
}


/* duplicate the ticker text once so the CSS animation loops with no gap
   the animation moves left by 50 percent so we need exactly 2 copies
   original content plus one identical copy equals two halves */
function makeTicker() {
  var ticker = document.querySelector(".ticker-track");
  if (!ticker) return;
  var original = ticker.innerHTML;
  ticker.innerHTML = original + original;
}


/* run everything once the HTML has fully loaded */
document.addEventListener("DOMContentLoaded", function () {

  /* read the saved theme or default to light */
  var saved = localStorage.getItem("outofstockTheme") || "light";
  changeTheme(saved);

  /* also update which dot button looks active */
  var activeBtn = document.querySelector("[data-theme=" + saved + "]");
  if (activeBtn) {
    document.querySelectorAll("[data-theme]").forEach(function (b) {
      b.classList.remove("is-active");
    });
    activeBtn.classList.add("is-active");
  }

  setupThemeButtons();
  mouseGlow();
  makeTicker();
});
