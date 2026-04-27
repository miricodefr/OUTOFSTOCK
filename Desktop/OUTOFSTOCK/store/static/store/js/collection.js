// collection page

$(document).ready(function() {

    // when user picks a category, load its subcategories
    $('#category-select').on('change', function() {
        var parentId = $(this).val();

        if (!parentId) {
            $('#subcategory-wrap').hide();
            return;
        }

        $.ajax({
            url: '/api/subcategories/',
            type: 'GET',
            data: { parent_id: parentId },
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(data) {
                if (data.subcategories.length > 0) {
                    var opts = '<option value="">All sub-categories</option>';
                    for (var i = 0; i < data.subcategories.length; i++) {
                        opts += '<option value="' + data.subcategories[i].id + '">' + data.subcategories[i].name + '</option>';
                    }
                    $('#subcategory-select').html(opts);
                    $('#subcategory-wrap').show();
                } else {
                    $('#subcategory-wrap').hide();
                }
            }
        });
    });

    // live filter as user types in search box
    $('[data-search]').on('input', function() {
        var q = $(this).val().toLowerCase();
        $('.catalog-card').each(function() {
            if ($(this).text().toLowerCase().includes(q)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

});
