// login page - basic validation before submitting

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('.auth-form');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        var username = document.querySelector('[name=username]');
        var password = document.querySelector('[name=password]');
        if (!username.value || !password.value) {
            e.preventDefault();
            alert('Please fill in both fields.');
        }
    });
});
