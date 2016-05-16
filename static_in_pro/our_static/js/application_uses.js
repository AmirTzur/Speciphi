$(document).ready(function () {
    // click on list will display selected type
    $('div#mobile_uses_list ul li').on('click', function () {
        var pressed_use = $(this).prop('id');
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
        // // get level should be shown to user # move to someplace else...
        // console.log($('div#uses_display').children().filter(function () {
        //     return 'list_use_' + $(this).prop('id') == pressed_use;
        // }).children('div.use_levels').attr('data-brand'));
    });
    // show pre-selected (by algorithm) level use description
    $('div#uses_display').children().each(function () {
        // get pre-selected level
        var pre_selected_use = $(this).children('div.use_levels').attr('data-brand');
        // show description
        $(this).children('div.use_levels').children('span#description_' + pre_selected_use).css('display', 'block');
    });


    // responsive query
    function WidthChange() {
        // mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            // show first use
            $('div#uses_display div').first().css('display', 'inline-block');


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
