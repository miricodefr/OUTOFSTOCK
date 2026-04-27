// runs on every page

// change the color theme
function changeTheme(theme) {
    document.body.classList.remove('theme-light', 'theme-dark', 'theme-orange');
    document.body.classList.add('theme-' + theme);
    localStorage.setItem('outofstockTheme', theme);
}

// set up the theme buttons
function setupThemeButtons() {
    var buttons = document.querySelectorAll('[data-theme]');
    buttons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            changeTheme(btn.dataset.theme);
            buttons.forEach(function(b) { b.classList.remove('is-active'); });
            btn.classList.add('is-active');
        });
    });
}

// make the orange circle follow the mouse
function mouseGlow() {
    var glow = document.querySelector('.cursor-glow');
    if (!glow) return;
    window.addEventListener('mousemove', function(e) {
        glow.style.opacity = '1';
        glow.style.left = e.clientX + 'px';
        glow.style.top = e.clientY + 'px';
    });
}

// the ticker needs to be duplicated so the animation loops without a gap
// the CSS moves it left by 50% so we need exactly 2 copies of the content
function makeTicker() {
    var ticker = document.querySelector('.ticker-track');
    if (!ticker) return;
    var original = ticker.innerHTML;
    ticker.innerHTML = original + original;
}

document.addEventListener('DOMContentLoaded', function() {
    var saved = localStorage.getItem('outofstockTheme') || 'light';
    changeTheme(saved);

    var activeBtn = document.querySelector('[data-theme=' + saved + ']');
    if (activeBtn) {
        document.querySelectorAll('[data-theme]').forEach(function(b) { b.classList.remove('is-active'); });
        activeBtn.classList.add('is-active');
    }

    setupThemeButtons();
    mouseGlow();
    makeTicker();
});
