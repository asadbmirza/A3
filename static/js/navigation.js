$(document).ready(function() {
    $('.nav-link').click(function(e) {
        e.preventDefault();
        const url = $(this).attr('href');
        const target = $(this).data('target');

        $.get(url, function(data) {
            $('#block-content').html($(data).find('#block-content').html());
            
            $('.nav-link').removeClass('active');
            $(this).addClass('active');
            
            history.pushState(null, null, url);
        }).fail(function() {
            console.error("Error loading page");
        });
    });

    $(window).on('popstate', function() {
        $.get(location.pathname, function(data) {
            $('#block-content').html($(data).find('#block-content').html());
        });
    });
});