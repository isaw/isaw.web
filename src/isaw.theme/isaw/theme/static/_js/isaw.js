jQuery(function($) {
	$('h3.trigger').click(function(){
		$(this).toggleClass('open');
		$('#main-navigation').toggleClass('open');
	});
});