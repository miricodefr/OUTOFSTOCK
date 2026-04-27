// cart page - ask for confirmation before removing items

$(document).ready(function() {
    $('[data-remove-link]').on('click', function(e) {
        if (!confirm('Remove this item from your cart?')) {
            e.preventDefault();
        }
    });
});
