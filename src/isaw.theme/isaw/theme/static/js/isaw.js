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
        $slides.css('height', 'auto');

        $slide_list.width($slides.width()*slide_count);
        $slide_list.css('max-width', 100*slide_count + '%');
        $slides.css('max-width', 100/slide_count + '%');
        $slides.css('max-width', 100/slide_count + '%');

        $slider_containers.css('max-width', $(window).width());
        $slider_containers.css('max-height', $slides.height());
    }
    // Ideally we would listen for window resizes, but EasySlider sets the
    // width for scrolling one time only.
    resize_slider();
    $(window).load(resize_slider);
});
