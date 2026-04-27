// dashboard scripts

function openModal() {
    $('.modal-overlay').addClass('is-open');
}

function closeModal() {
    $('.modal-overlay').removeClass('is-open');
}

function toggleEdit(id) {
    $('[data-edit-form=' + id + ']').toggleClass('is-open');
}

function toggleCatEdit(id) {
    $('[data-edit-cat-form=' + id + ']').toggleClass('is-open');
}

$(document).ready(function() {

    $('[data-open-modal]').on('click', openModal);
    $('.modal-close').on('click', closeModal);

    // close modal when clicking the dark background
    $('.modal-overlay').on('click', function(e) {
        if ($(e.target).hasClass('modal-overlay')) {
            closeModal();
        }
    });

    $('[data-edit-btn]').on('click', function() {
        toggleEdit($(this).data('edit-btn'));
    });

    $('[data-edit-cat]').on('click', function() {
        toggleCatEdit($(this).data('edit-cat'));
    });

    $('[data-delete-listing]').on('click', function(e) {
        if (!confirm('Delete this listing?')) {
            e.preventDefault();
        }
    });

    $('[data-delete-user]').on('click', function(e) {
        if (!confirm('Delete this user?')) {
            e.preventDefault();
        }
    });

    // image preview for the new listing form
    $('#modal-image-input').on('change', function() {
        var strip = $('#modal-preview-strip');
        strip.empty();
        var files = this.files;
        for (var i = 0; i < files.length; i++) {
            var reader = new FileReader();
            // need to wrap in a function because of the loop
            (function(index) {
                reader.onload = function(e) {
                    var cls = index === 0 ? 'preview-thumb is-cover' : 'preview-thumb';
                    strip.append('<div class="' + cls + '"><img src="' + e.target.result + '" /></div>');
                };
            })(i);
            reader.readAsDataURL(files[i]);
        }
    });

    // recently viewed carousel
    var pos = 0;
    var track = $('#recentTrack');

    if (track.length) {
        $('#recentNext').on('click', function() {
            var cardW = track.find('.recent-card').first().outerWidth(true) + 16;
            var maxPos = track[0].scrollWidth - track.parent().width();
            pos = Math.min(maxPos, pos + cardW * 3);
            track.css('transform', 'translateX(-' + pos + 'px)');
            updateArrows();
        });

        $('#recentPrev').on('click', function() {
            var cardW = track.find('.recent-card').first().outerWidth(true) + 16;
            pos = Math.max(0, pos - cardW * 3);
            track.css('transform', 'translateX(-' + pos + 'px)');
            updateArrows();
        });

        function updateArrows() {
            var maxPos = track[0].scrollWidth - track.parent().width();
            if (pos <= 0) {
                $('#recentPrev').addClass('hidden');
            } else {
                $('#recentPrev').removeClass('hidden');
            }
            if (pos >= maxPos) {
                $('#recentNext').addClass('hidden');
            } else {
                $('#recentNext').removeClass('hidden');
            }
        }

        updateArrows();
    }

});
