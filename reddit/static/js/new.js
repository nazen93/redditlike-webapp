$(function() {
	$('.nav-tabs > li').on('click', function() {
		$(this).siblings().removeClass('active');
		$(this).addClass('active');
	});
	
});