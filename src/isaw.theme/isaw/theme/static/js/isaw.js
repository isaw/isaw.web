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
    var $slider_containers = $('#slider-container, #slider');
    var $slides = $('#slider .slide');
    var $images = $('#slider .slide img');
    function resize_slider() {
        var $slide_list = $('#slider .slider-list');
        var slide_count = $slides.length;

        $slides.css('width', $(window).width()).css('height', 'auto');
        $images.css('width', '100%').css('height', 'auto');

        $slide_list.width($slides.width()*slide_count);
        $slide_list.css('max-width', 100*slide_count + '%');
        $slides.css('max-width', 100/slide_count + '%');

        $slider_containers.css('width', $(window).width());
        $slider_containers.css('height', $slides.height());
    }
    // Ideally we would listen for window resizes, but EasySlider sets the
    // width for scrolling one time only.
    resize_slider();
    $(window).load(resize_slider);
    $images.load(resize_slider);
    /*capture the search link click and open the drawer*/
    $('#secondary #siteaction-search a').click(function(e){
	   e.preventDefault();
	   $('#portal-searchbox').slideToggle();
    });
    
    /* close aliens invaded message */
    $('#emergency-message .close').click(function() {
        var date = new Date();
        date.setTime(date.getTime()+(1*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
        document.cookie = "isaw-emergency-read=yes"+expires+"; path=/";
        $(this).parent().hide();
    });
    
});
