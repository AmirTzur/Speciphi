$(document).ready(function () {
    // show first type # change to mobile only
    $('div#types_display div:nth-child(1)').css('display', 'block');
    // iterate checked checkboxes and show V on type list (needed when a user press back button) # change to mobile only
    $('div#types_display').children().filter(function () {
        if ($(this).children('div.choose_container').children('input[type=checkbox]').is(':checked')) {
            var checked_type = $(this).prop('id');
            // set V
            $('div#mobile_types_list ul').children().filter(function () {
                return $(this).context.innerText == checked_type;
            }).children().css('display', 'inline');
        }
    });
    // click on list will change displayed type # change to mobile only
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
            return $(this).prop('id') == pressed_type;
        }).css('display', 'block');
    });
    // on checkbox changed, set or remove V #change to mobile only
    $(':checkbox').change(function () {
        var checked_type = $(this).prop('name');
        if ($(this).is(":checked")) {
            // set V
            $('div#mobile_types_list ul').children().filter(function () {
                return $(this).context.innerText == checked_type;
            }).children().css('display', 'inline');
        }
        else {
            // remove V
            // inner <i> adds a weird space at beginning of innerText - remove it
            $('div#mobile_types_list ul').children().filter(function () {
                var mobile_list_type = $(this).context.innerText;
                if (!(/^[0-9a-zA-Z]+$/.test(mobile_list_type.charAt(0)))) {
                    mobile_list_type = mobile_list_type.substring(1);
                }
                return mobile_list_type == checked_type;
            }).children().css('display', 'none');
        }
        // run SQL procedure
        AJAX_setNewConsulteeAffiliation(this);
    });
    // change checkbox value when choose_text clicked
    $('.checkbox_text').click(function () {
        $(this).parent().parent().children('button').children('input[type=checkbox]').prop('checked', !$(this).parent().parent().children('button').children('input[type=checkbox]').is(':checked')).change();
    });
    // change checkbox value when button or clicked
    $('div#types_display div button').click(function () {
        $(this).children('input[type=checkbox]').prop('checked', !$(this).children('input[type=checkbox]').is(':checked')).change();
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