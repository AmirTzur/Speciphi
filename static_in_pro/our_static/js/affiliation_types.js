$(document).ready(function () {
    // show first type # change to mobile only
    $('div#types_display div:nth-child(2)').css('display', 'block');
    $('div#mobile_types_list ul li:first-child').css('padding-top', '15px');
    // change displayed type on list item clicked # change to mobile only
    $('div#mobile_types_list ul li').on('click', function () {
        // get pressed type
        var pressed_type = $(this).context.innerText;
        // change displayed type to display: none
        $('div#types_display').children().filter(function () {
            return $(this).css('display') == 'block';
        }).css('display', 'none');
        // change pressed type css to display: block
        $('div#types_display').children().filter(function () {
            return $(this).attr('id') == pressed_type;
        }).css('display', 'block');
    });
});