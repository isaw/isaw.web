/*global google:true, jQuery:true*/
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
    
    var $location_edit = $('.googleMapEdit, .geolocation_wrapper.edit');
    if ($location_edit.length) {
        var $pleiades_widget = $('<div class="pleiades-location"><label>Fetch coordinates from Pleiades URL</label><input type="text" /><button class="PleiadesFetch">Fetch</button><div>');
        $location_edit.append($pleiades_widget);
        $pleiades_widget.find('button').on('click',
            function (e) {
                e.preventDefault();
                e.stopPropagation();
                var $input = $(this).siblings('input');
                var url = $input.val();
                $.getJSON(url,
                    function (data) {
                        var repr_point = data.reprPoint;
                        if (repr_point) {
                            $location_edit.find('input#geolocation_latitude, input.geolocationfield-field.latitude').val(repr_point[1]);
                            $location_edit.find('input#geolocation_longitude, input.geolocationfield-field.longitude').val(repr_point[0]);
                            $input.val('');
                        } else {
                            window.alert('No representative point found in response');
                        }
                    }
                ).error(function () {window.alert('Error fetching ' + url);});
                return false;
            }
        );
    }
    var $maps = $('.template-view #content div.geolocation_wrapper .map');

    var _loadgmap = function(){
        var source,
            script = document.createElement("script");

        script.type = "text/javascript";
        source = "https://maps.google.com/maps/api/js?libraries=geometry&sensor=false&callback=initialize_maps&language=" + window.mapsConfig.i18n.language ;
        if (window.mapsConfig.googlemaps_keys.length){
            source += '&key=' + window.mapsConfig.googlemaps_keys;
        }
        script.src = source;

        document.body.appendChild(script);
    };
    var _init_maps = function () {
        $maps.each(function() {
            var $map = $(this);
            var coord_info = $map.data('geopoints')[0];
            var pos = {lat: coord_info.lat, lng: coord_info.lng};
            var map_options = {
                mapTypeId: window.mapsConfig.settings.maptype || google.maps.MapTypeId.ROADMAP,
                center: pos,
                zoom: window.mapsConfig.settings.zoom || 7
            };
            var map = new google.maps.Map($map.get(0), map_options);
            var marker = new google.maps.Marker({title: coord_info.popup, position: pos, map: map});
        });
    };
    if ($maps.length) {
        window.initialize_maps = _init_maps;
        _loadgmap();
    }
    var $lat = $('input.geolocation-widget.latitude, input#geolocation_latitude');
    if ($lat.length) {
        $lat.wrap('<div />').parent().prepend('<label for="'+$lat.attr('id')+'">latitude:</label> ');
    }
    var $long = $('input.geolocation-widget.longitude, input#geolocation_longitude');
    if ($long.length) {
        $long.wrap('<div />').parent().prepend('<label for="'+$long.attr('id')+'">longitude:</label> ');
    }
});
