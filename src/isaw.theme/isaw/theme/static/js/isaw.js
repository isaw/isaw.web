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
        var $slides = $('#slider .slide');
        var $slide_list = $('#slider .slider-list');
        var slide_count = $slides.length;

        $slides.css('max-width', $(window).width());

        $slide_list.width($slides.width()*slide_count);
        $slide_list.css('max-width', 100*slide_count + '%');
        $slides.css('max-width', 100/slide_count + '%');
        $slides.css('max-width', 100/slide_count + '%');
        $slides.css('max-height', $slides.height());

        $slider_containers.css('max-width', $(window).width());
        $slider_containers.css('max-height', $slides.height());
    }
    resize_slider();
    $( window ).resize(resize_slider);
});
