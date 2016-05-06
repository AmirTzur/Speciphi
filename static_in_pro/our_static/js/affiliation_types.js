$(document).ready(function () {
    // extra small and small screens build up
    if ($(window).width() < 992) {
        // show first type # mobile only
        $('div#types_display div:nth-child(1)').css('display', 'block');
        // color checked types on type list (needed when a user press back button) # mobile only
        $('div#types_display').children().filter(function () {
            if ($(this).children('button.type_button').children('input[type=checkbox]').is(':checked')) {
                var checked_type = $(this).prop('id');
                // change color
                $('div#mobile_types_list ul').children().filter(function () {
                    return $(this).context.innerText == checked_type;
                }).css('color', 'black');
            }
        });
        // click on list will display selected type # mobile only
        $('div#mobile_types_list ul li').on('click', function () {
            var pressed_type = $(this).context.innerText;
            // inner <i> adds a space at beginning of innerText - remove it
            if (!(/^[0-9a-zA-Z]+$/.test(pressed_type.charAt(0)))) {
                pressed_type = pressed_type.substring(1);
            }
            // hide current displayed type
            $('div#types_display').children().filter(function () {
                return $(this).css('display') == 'block';
            }).css('display', 'none');
            // show pressed type
            $('div#types_display').children().filter(function () {
                return $(this).prop('id') == pressed_type;
            }).css('display', 'block');
        });
        // on checkbox changed, set or remove type list color # mobile only
        $(':checkbox').change(function () {
            var checked_type = $(this).prop('name');
            if ($(this).is(":checked")) {
                // set list color
                $('div#mobile_types_list ul').children().filter(function () {
                    return $(this).context.innerText == checked_type;
                }).css('color', 'black');
            }
            else {
                // remove type list color
                $('div#mobile_types_list ul').children().filter(function () {
                    var mobile_list_type = $(this).context.innerText;
                    // inner <i> adds a weird space at beginning of innerText - remove it
                    if (!(/^[0-9a-zA-Z]+$/.test(mobile_list_type.charAt(0))))
                        mobile_list_type = mobile_list_type.substring(1);
                    return mobile_list_type == checked_type;
                }).css('color', 'white');
            }
        });
    }

    // change checkbox value when button clicked
    $('div#types_display div button').click(function () {
        $(this).children('input[type=checkbox]').prop('checked', !$(this).children('input[type=checkbox]').is(':checked')).change();
    });
    // invoke setNewConsulteeAffiliation when select or remove affiliation
    $(':checkbox').change(function () {
        // run SQL procedure
        AJAX_setNewConsulteeAffiliation(this);
    });
    function AJAX_setNewConsulteeAffiliation(object) {
        // convert check from true/false to 1/0
        var checked_val;
        if ($(object).is(':checked')) checked_val = 1;
        else checked_val = 0;
        // send AJAX post request to NewConsulteeAffiliation view
        $.ajax({
            url: '/NewConsulteeAffiliation/', // the endpoint
            type: "POST", // http method
            data: {Affiliation_id: $(object).val(), checked: checked_val}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                //console.log(json); // log the returned json to the console
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText, errmsg, err); // provide a bit more info about the error to the console
            }
        });
    }
});


//// locate next_page button in the middle of screen
//$('#next_page').css('bottom', parseInt((parseInt($('#types_wrapper').css('height')) - parseInt($('#next_page').css('height'))) / 2) + 'px');