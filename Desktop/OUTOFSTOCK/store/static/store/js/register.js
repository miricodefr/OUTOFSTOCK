// register page - validate the form before it submits

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('.auth-form');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        var username = document.querySelector('[name=username]');
        var email = document.querySelector('[name=email]');
        var password = document.querySelector('[name=password]');

        if (!username.value || !email.value || !password.value) {
            e.preventDefault();
            alert('All fields are required.');
            return;
        }

        if (!email.value.includes('@')) {
            e.preventDefault();
            alert('Please enter a valid email address.');
            return;
        }

        if (password.value.length < 6) {
            e.preventDefault();
            alert('Password must be at least 6 characters long.');
        }
    });
});
