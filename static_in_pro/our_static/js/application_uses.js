$(document).ready(function () {
    // click on list will display selected type
    $('div#mobile_uses_list ul li').on('click', function () {
        var pressed_use = $(this).prop('id');
        console.log(pressed_use);
        // inner <i> adds a space at beginning of innerText - remove it
        if (!(/^[0-9a-zA-Z]+$/.test(pressed_use.charAt(0)))) {
            pressed_use = pressed_use.substring(1);
        }
        // hide current displayed type
        $('div#uses_display').children().filter(function () {
            return $(this).css('display') == 'inline-block';
        }).css('display', 'none');
        // show pressed type
        $('div#uses_display').children().filter(function () {
            return 'list_use_' + $(this).prop('id') == pressed_use;
        }).css('display', 'inline-block');
    });


    // responsive query
    function WidthChange() {
        // mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            // show first use
            $('div#uses_display div:nth-child(1)').css('display', 'inline-block');
            $('div#uses_display div:nth-child(1)').children('div').css('display', 'block');



        } //end mobile screens
        // desktop screens
        else if (window.matchMedia("(min-width: 992px)").matches) {


        }//end desktop screens
    }// end responsive query

    // media query event handler
    if (matchMedia) {
        // define break points
        var mq_mobile = window.matchMedia("(max-width: 991px)");
        // add listeners and callback
        mq_mobile.addListener(WidthChange);
        // invoke layout function
        WidthChange();
    }

});
