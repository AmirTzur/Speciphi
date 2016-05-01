$(document).ready(function () {
    // show first type # change to mobile only
    $('div#types_display div:nth-child(1)').css('display', 'block');
    // fix padding
    $('div#mobile_types_list ul li:first-child').css('padding-top', '15px');
    // click on list change displayed type # change to mobile only
    $('div#mobile_types_list ul li').on('click', function () {
        // get pressed type
        var pressed_type = $(this).context.innerText;
        // inner <i> adds a space at beginning of innerText - remove it
        if (!(/^[0-9a-zA-Z]+$/.test(pressed_type.charAt(0)))) {
            pressed_type = pressed_type.substring(1);
        }
        // change displayed type to display: none
        $('div#types_display').children().filter(function () {
            return $(this).css('display') == 'block';
        }).css('display', 'none');
        // change pressed type css to display: block
        $('div#types_display').children().filter(function () {
            return $(this).attr('id') == pressed_type;
        }).css('display', 'block');
    });
    // on checkbox changed, set or remove V #change to mobile only
    $(':checkbox').change(function () {
        var checked_type = $(this).attr('name');
        console.log(checked_type);
        if ($(this).is(":checked")) {
            // set V
            console.log('checked');
            $('div#mobile_types_list ul').children().filter(function () {
                return $(this).context.innerText == checked_type;
            }).children().css('display', 'inline');
        }
        else {
            // remove V
            console.log('unchecked');
            // inner <i> adds a weird space at beginning of innerText - remove it
            $('div#mobile_types_list ul').children().filter(function () {
                var mobile_list_type = $(this).context.innerText;
                if (!(/^[0-9a-zA-Z]+$/.test(mobile_list_type.charAt(0)))) {
                    mobile_list_type = mobile_list_type.substring(1);
                }
                console.log(mobile_list_type + ',' + checked_type);
                return mobile_list_type == checked_type;
            }).children().css('display', 'none');
        }
    });

});