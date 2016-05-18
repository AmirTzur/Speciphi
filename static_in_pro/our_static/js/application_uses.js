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
    });

    // on button click, change checkbox value
    $('div#uses_display div button').click(function () {
        // change pressed checkbox
        $(this).children('input[type=checkbox]').prop('checked', !$(this).children('input[type=checkbox]').is(':checked')).change();
    });

    $(':checkbox').change(function () {
        // color text of pressed button
        if ($(this).is(':checked')) {
            $(this).parent('button').css('color', 'rgb(230, 89, 42)');
        } else {
            $(this).parent('button').css('color', 'rgb(249, 163, 51)');
        }

        // get pressed level of use
        var selected_use_level = $(this).prop('value');
        console.log(selected_use_level);
        // change to matched description
        $(this).parent().parent().children('span').each(function () {
            if ($(this).prop('id') == 'description_' + selected_use_level) {
                $(this).css('display', 'block');
            }
            else {
                $(this).css('display', 'none');
            }
        });
        // cancel other checked levels checkbox
        $(this).parent().parent().children('button').each(function () {
            if ($(this).children('input[type=checkbox]').prop('value') != selected_use_level) {
                $(this).children('input[type=checkbox]').prop('checked', false);
                // change button text to default color
                $(this).css('color', 'rgb(249, 163, 51)');
            }
        });
        console.log($(this).prop('checked'));
    });

    // show pre-selected (by algorithm) level of use description
    $('div#uses_display').children().each(function () {
        // get pre-selected level
        var pre_selected_use = $(this).children('div.use_levels').attr('data-brand');
        // check right checkbox (this will activate description change)
        $(this).children('div.use_levels').children('button').each(function () {
            if ($(this).attr('value') == pre_selected_use) {
                $(this).children('input[type=checkbox]').prop('checked', true).change();
            }
        });
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
