$(function() {
	$('#under-post > .not-active').on('click', function() {
		$(this).parent().siblings('form').submit();
	});
});