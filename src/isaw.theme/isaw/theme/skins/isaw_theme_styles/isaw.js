$(window).load(function(){
    // initialize scrollable
    $(function(){ 
        $(".scrollable").scrollable({circular: true}).autoscroll({interval: 10000});
    });

    // set width on image <dl>s to be set at the width of the image
    // to keep caption from pushing out the width
    var capnum = $("dl.captioned").length;

    for(var i = 0; i < capnum; i++) {
         var imgWidth = $("dl.captioned img").eq(i).width();
         $("dl.captioned").css("width",imgWidth);
    }
    
    // align faculty e-mail/info link to bottom of image if text isn't too tall
    for(i = 0; i < $(".facultyListing").length; i++) {
       var imageHeight = $(".facultyListing img").eq(i).height() + 12;
       var descripHeight = $(".facultyInfo").eq(i).height();
       if (descripHeight > imageHeight) {
           $(".facultyListing .alignBottom").eq(i).css("position","relative");
       }
    }
});
