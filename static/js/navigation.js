$(document).ready(function() {

    const currentPath = window.location.pathname;

    $('.nav-links a').each(function() {
        const linkPath = $(this).attr('href');
        if ((linkPath === '/' && currentPath === '/') || (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }
    });

    const enableDarkMode = () => {
        $('body').addClass('dark-mode');
        $('nav').addClass('dark-mode');
        $('footer').addClass('dark-mode');
        localStorage.setItem('darkMode', 'enabled');
    }

    const disableDarkMode = () => {
        $('body').removeClass('dark-mode');
        $('nav').removeClass('dark-mode');
        $('footer').removeClass('dark-mode');
        localStorage.setItem('darkMode', 'disabled');
    }

    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
        $('#darkmode-toggle').prop('checked', true);
    }

    $('#darkmode-toggle').click(function() {
        if ($('body').hasClass('dark-mode')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    });
});