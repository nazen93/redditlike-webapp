$('.nav-pills > li > a').click( function() {
    $('.nav-pills > li.active').removeClass('active');
    $(this).parent().addClass('active');
} );