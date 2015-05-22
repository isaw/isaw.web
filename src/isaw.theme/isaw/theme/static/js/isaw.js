jQuery(function($) {
	$('h3.trigger').click(function(){
		$(this).toggleClass('open');
		$('#main-navigation').toggleClass('open');
	});
    var nav_folders = $('ul.navTree li.navTreeFolderish');
    nav_folders.each(function (i, e) {
        var folder = $(e);
        if (folder.children().length < 2) {
            folder.addClass('collapsed');
        }
    });
    function resize_slider() {
        var $slider_containers = $('#slider-container, #slider');
        var $slider_images = $('#slider img');
        $slider_images.css('max-width', $(window).width());
        $slider_containers.css('max-width', $(window).width());
        $slider_containers.css('max-height', $slider_images.height());
    }
    resize_slider();
    $( window ).resize(resize_slider);
});
