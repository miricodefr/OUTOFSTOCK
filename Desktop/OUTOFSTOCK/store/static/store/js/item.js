// product detail page

$(document).ready(function() {

    // gallery navigation
    var currentIndex = 0;
    var thumbs = $('#thumbStrip .thumb-btn');
    var totalImages = thumbs.length;
    var urls = [];

    thumbs.each(function() {
        urls.push($(this).data('src'));
    });

    function goTo(index) {
        if (index < 0) index = totalImages - 1;
        if (index >= totalImages) index = 0;
        currentIndex = index;

        // fade out then change image
        $('#main-img-tag').addClass('fading');
        setTimeout(function() {
            $('#main-img-tag').attr('src', urls[currentIndex]);
            $('#main-img-tag').removeClass('fading');
        }, 220);

        // update which thumbnail is highlighted
        thumbs.removeClass('thumb-active');
        thumbs.eq(currentIndex).addClass('thumb-active');

        // update dots
        $('.gallery-dot').removeClass('active');
        $('.gallery-dot').eq(currentIndex).addClass('active');

        // scroll the strip so the thumb is visible
        var strip = document.getElementById('thumbStrip');
        if (strip) {
            var t = thumbs.eq(currentIndex)[0];
            if (t.offsetLeft < strip.scrollLeft) {
                strip.scrollLeft = t.offsetLeft - 8;
            } else if (t.offsetLeft + t.offsetWidth > strip.scrollLeft + strip.offsetWidth) {
                strip.scrollLeft = t.offsetLeft + t.offsetWidth - strip.offsetWidth + 8;
            }
        }
    }

    $('#galleryPrev').on('click', function(e) {
        e.preventDefault();
        goTo(currentIndex - 1);
    });

    $('#galleryNext').on('click', function(e) {
        e.preventDefault();
        goTo(currentIndex + 1);
    });

    thumbs.on('click', function(e) {
        e.preventDefault();
        goTo(parseInt($(this).data('index')));
    });

    $('.gallery-dot').on('click', function(e) {
        e.preventDefault();
        goTo(parseInt($(this).data('index')));
    });

    $(document).on('keydown', function(e) {
        if (e.key === 'ArrowLeft') goTo(currentIndex - 1);
        if (e.key === 'ArrowRight') goTo(currentIndex + 1);
    });

    // star rating keyboard support
    $('.star-picker label').attr('tabindex', '0').on('keydown', function(e) {
        if (e.key === 'Enter') $(this).trigger('click');
    });

    // review form via AJAX
    $('#review-form').on('submit', function(e) {
        e.preventDefault();

        var rating = $('input[name=rating]:checked').val();
        if (!rating) {
            $('#review-error').text('Please pick a star rating.').show();
            return;
        }

        var btn = $(this).find('button[type=submit]');
        btn.prop('disabled', true).text('Submitting...');
        $('#review-error').hide();

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(data) {
                if (data.ok) {
                    // update the average stars
                    var filled = Math.round(data.new_avg);
                    var stars = '';
                    for (var i = 1; i <= 5; i++) {
                        stars += i <= filled ? '&#9733;' : '&#9734;';
                    }
                    $('.avg-stars').html(stars);
                    $('.rating-title').text('Average rating  ' + data.new_avg + ' out of 5');
                    $('.review-count-text').text(data.count + ' reviews');
                    $('.rating-box').show();

                    // add the review to the top of the list
                    var rStars = '';
                    for (var j = 1; j <= 5; j++) {
                        rStars += j <= data.rating ? '&#9733;' : '&#9734;';
                    }
                    var html = '<div class="review-block">'
                        + '<strong>' + data.username + '</strong>'
                        + '<span class="review-stars">' + rStars + '</span>'
                        + (data.comment ? '<p style="margin-top:0.4rem;">' + data.comment + '</p>' : '')
                        + '</div>';
                    $('.no-reviews-msg').remove();
                    $('.review-section .review-block:first').before(html);

                    // hide the form
                    $('.review-form-wrap').html('<p style="color:var(--green);">Thanks for your review!</p>');
                } else {
                    $('#review-error').text(data.error).show();
                    btn.prop('disabled', false).text('Submit Review');
                }
            },
            error: function() {
                $('#review-error').text('Something went wrong, please try again.').show();
                btn.prop('disabled', false).text('Submit Review');
            }
        });
    });

});
