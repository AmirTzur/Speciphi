$(document).ready(function () {
    // responsive query
    function WidthChange() {

        // mobile screens
        if (window.matchMedia("(max-width: 767px)").matches) {
            console.log('mobile', $(window).width());

            $('#company_description').addClass('reverse_wrapper');
            $('#company_video_wrapper').addClass('reverse_first');
            $('#company_description_wrapper').addClass('reverse_second');
        } //end mobile screens
        // desktop screens
        else if (window.matchMedia("(min-width: 767px)").matches) {
            console.log('desktop', $(window).width());
            $('#company_description').removeClass('reverse_wrapper');
            $('#company_video_wrapper').removeClass('reverse_first');
            $('#company_description_wrapper').removeClass('reverse_second');
        }//end desktop screens
    }// end responsive query

// media query event handler
    if (matchMedia) {
        // define break points
        var mq_mobile = window.matchMedia("(max-width: 767px)");
        // add listeners and callback
        mq_mobile.addListener(WidthChange);
        // invoke layout function
        WidthChange();
    }
});