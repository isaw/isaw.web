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
});