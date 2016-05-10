$(document).ready(function () {
    // click on list will display selected type
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
    // on checkbox change, set or remove type list color
    $(':checkbox').change(function () {
        var checked_type = $(this).prop('name');
        if ($(this).is(":checked")) {
            // set list color
            $('div#mobile_types_list ul').children().filter(function () {
                return $(this).context.innerText == checked_type;
            }).css('color', '#E6592A');
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
    // on button click, change checkbox value
    $('div#types_display div button').click(function () {
        $(this).children('input[type=checkbox]').prop('checked', !$(this).children('input[type=checkbox]').is(':checked')).change();
    });
    // invoke setNewConsulteeAffiliation when check or !check affiliation
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

    // responsive query
    function WidthChange() {
        // mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            // show type list
            $('div#mobile_types_list').css('display', 'block');
            // if was in desktop layout - move types back to .types_display and delete #types_first&second_row
            if ($('div#types_display div:nth-child(1)').hasClass('row')) {
                $('div#types_first_row').children().each(function (index) {
                    // show description and add it back to default place
                    $(this).children('button').children('span').css('display', 'block');
                    $(this).children('button').children('span').appendTo($(this));
                    if (index == 0) {
                        $(this).css('display', 'block');
                    }
                    else {
                        $(this).css('display', 'none');
                    }
                    $(this).appendTo('div#types_display');
                });
                $('div#types_second_row').children().each(function () {
                    $(this).children('button').children('span').css('display', 'block');
                    $(this).children('button').children('span').appendTo($(this));
                    $(this).css('display', 'none');
                    $(this).appendTo('div#types_display');
                });
                //delete rows
                $('div#types_first_row').remove();
                $('div#types_second_row').remove();
            }
            else {
                // show first type
                $('div#types_display div:nth-child(1)').css('display', 'block');
            }
            // color checked types on type list (needed also when a user press back button)
            $('div#types_display').children().filter(function () {
                if ($(this).children('button.type_button').children('input[type=checkbox]').is(':checked')) {
                    var checked_type = $(this).prop('id');
                    // change color
                    $('div#mobile_types_list ul').children().filter(function () {
                        return $(this).context.innerText == checked_type;
                    }).css('color', '#E6592A');
                }
            });

        } //end mobile screens
        // desktop screens
        else if (window.matchMedia("(min-width: 992px)").matches) {
            // hide type list
            $('div#mobile_types_list').css('display', 'none');
            // insert types into rows
            if ($('div#types_display div:nth-child(1)').hasClass('type_display')) {
                // create first & second rows divs
                $('div#types_display').prepend('<div id="types_first_row" class="row"></div><div id="types_second_row" class="row"></div>');
                // iterate types
                $('div#types_display').children().each(function (index) {
                    // hide description and insert it into button
                    $(this).children('span').css('display', 'none');
                    $(this).children('span').appendTo($(this).children('button'));
                    // show type
                    $(this).css('display', 'inline-block');
                    // insert types into rows (divs 0 and 1 are types rows)
                    //01|2345|6789
                    if (index > 1 && index < 6)
                        $(this).appendTo('div#types_first_row');
                    else if (index > 5 && index < 10) {
                        $(this).appendTo('div#types_second_row');
                    } else if (index > 9) {
                        alert("wired.. got more then 8 types?!");
                    }
                });
            }
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

//var mq_xs = window.matchMedia("(max-width: 767px)");
//var mq_md = window.matchMedia("(min-width: 992px) and (max-width: 1199px)");
//if (window.matchMedia("(max-width: 767px)").matches) {//extra-small screens
//}
//else if (window.matchMedia("(min-width: 768px) and (max-width: 991px)").matches) {//small screens
//}
//else if (window.matchMedia("(min-width: 992px) and (max-width: 1199px)").matches) {//medium screens
//}
//else if (window.matchMedia("(min-width: 1200px)").matches) {//large screens
//}