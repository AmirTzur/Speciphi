$(document).ready(function () {

    // click on list will display selected type
    $('div#mobile_uses_list ul li').on('click', function () {
        var pressed_use = $(this).prop('id');
        // inner <i> adds a space at beginning of innerText - remove it
        if (!(/^[0-9a-zA-Z]+$/.test(pressed_use.charAt(0)))) {
            pressed_use = pressed_use.substring(1);
        }
        // hide current displayed use
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

    // checkbox change
    $(':checkbox').change(function () {
        // get pressed level of use
        var selected_use_level;
        // color text of pressed button
        if ($(this).is(':checked')) {
            $(this).parent('button').css('color', 'rgb(230, 89, 42)');
            selected_use_level = $(this).prop('value');
        } else {
            $(this).parent('button').css('color', 'rgb(249, 163, 51)');
            // un checked (use level 0)
            selected_use_level = '0'; // (temporary equals 1, on 0 no description
        }
        // update data-brand (where we keep algorithm choice value)
        $(this).parent('button').parent('div.use_levels').attr('data-brand', selected_use_level);
        // cancel other checked levels checkbox
        $(this).parent('button').parent('div.use_levels').children('button').each(function () {
            if ($(this).children('input[type=checkbox]').prop('value') != selected_use_level) {
                $(this).children('input[type=checkbox]').prop('checked', false);
                // change button text to default color
                $(this).css('color', 'rgb(249, 163, 51)');
            }
        });
        // show matched description # mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            $(this).parent().parent().children('span').each(function () {
                if ($(this).prop('id') == 'description_' + selected_use_level) {
                    $(this).css('display', 'block');
                }
                else {
                    $(this).css('display', 'none');
                }
            });
        }
        // update column buttons # desktop
        if (window.matchMedia("(min-width: 992px)").matches) {
            // update pressed column
            UpdateColumn($(this).parent('button').parent('div.use_levels'), selected_use_level);
        }
    }); // end checkbox change

    // show description text on *button hover* # desktop
    $('button.use_level_button').mouseenter(function () {
        if (window.matchMedia("(min-width: 992px)").matches) {
            // get pressed level of use
            var selected_use_level = $(this).prop('value');
            $(this).parent().children('span').each(function () {
                // update description div
                if ($(this).prop('id') == 'description_' + selected_use_level) {
                    $('#description_container').children('span').html($(this).html());
                }
            });
            // color buttons
            UpdateColumn($(this).parent('div.use_levels'), selected_use_level);
        }
    });
    // remove description text after *button hover* # desktop
    $('button.use_level_button').mouseleave(function () {
        if (window.matchMedia("(min-width: 992px)").matches) {
            $('#description_container').children('span').html('&nbsp;');
            // color buttons
            UpdateColumn($(this).parent('div.use_levels'), $(this).parent('div.use_levels').attr('data-brand'));
        }
    });

    // responsive query
    function WidthChange() {
        // mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            // hide all uses
            $('div#uses_display').children().each(function () {
                $(this).css('display', 'none');
            });
            // show first use
            $('div#uses_display div').first().css('display', 'inline-block');
            // if was on desktop switch back default use display and buttons order
            if ($('div#uses_display').children().first().children().first().hasClass('use_levels')) {
                // use_name to use_circle
                $('div#uses_display').children().each(function () {
                    $(this).children('div').last().removeClass('use_name');
                    $(this).children('div').last().addClass('use_circle');
                    $(this).children('div').last().prependTo(this);
                    // delete desktop description
                    $('#description_container').remove();
                });
                // show right description
                $('div#uses_display').children().each(function () {
                    // get selected level
                    var selected_use = $(this).children('div.use_levels').attr('data-brand');
                    // show right description
                    $(this).children('div.use_levels').children('span').each(function () {
                        if ($(this).prop('id') == 'description_' + selected_use) {
                            $(this).css('display', 'block');
                        }
                    });
                });
                // change buttons order back to default
                $('#uses_display').children('div.use_display').each(function () {
                    $($(this).children('div.use_levels').children('button').get().reverse()).each(function () {
                        $(this).parent('div').append(this);
                    });
                });
                // remove "desktop style" from buttons
                $('div.use_levels').children('button').removeClass('use_level_button_0 hide_text');
            }
        } //end mobile screens
        // desktop screens
        else if (window.matchMedia("(min-width: 992px)").matches) {
            // display uses in line
            $('div#uses_display').children().css('display', 'inline-block');
            // remove use_circle class and show name at the bottom
            $('div#uses_display').children().each(function () {
                $(this).children('div').first().removeClass('use_circle');
                $(this).children('div').first().addClass('use_name');
                $(this).children('div').first().appendTo(this);
            });
            // hide description text
            $('span.description_text').css('display', 'none');
            // add new description container
            $('div#uses_wrapper form').prepend('<div id="description_container"><span>&nbsp;</span></div>');
            // change use_levels buttons order
            $('#uses_display').children('div.use_display').each(function () {
                // iterate buttons in reverse order
                $($(this).children('div.use_levels').children('button').get().reverse()).each(function () {
                    $(this).parent('div').append(this);
                });
            });
            // hide use_level_buttons text (High/Med/Low)
            $('.use_level_button').addClass('hide_text');
            //  update buttons style
            $('div#uses_display').children('div.use_display').each(function () {
                // update buttons style
                UpdateColumn($(this).children('div.use_levels'), $(this).children('div.use_levels').attr('data-brand'));
            });
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

    // show pre-selected (by algorithm) level of use description
    $('div#uses_display').children('div.use_display').each(function () {
        // get pre-selected level
        var pre_selected_use = $(this).children('div.use_levels').attr('data-brand');
        // check right checkbox
        $(this).children('div.use_levels').children('button').each(function () {
            if ($(this).attr('value') == pre_selected_use) {
                $(this).children('input[type=checkbox]').prop('checked', true);
                // activate: description change # mobile, buttons style # desktop
                startChoices($(this).children('input[type=checkbox]'));
            }
        });
    });
    // show matched description
    function startChoices(that) {
        // color text of pressed button
        $(that).parent('button').css('color', 'rgb(230, 89, 42)');
        // get pressed level of use
        var selected_use_level = $(that).prop('value');
        // show matched description #mobile only
        if (window.matchMedia("(max-width: 991px)").matches) {
            $(that).parent().parent().children('span').each(function () {
                if ($(this).prop('id') == 'description_' + selected_use_level) {
                    $(this).css('display', 'block');
                }
                else {
                    $(this).css('display', 'none');
                }
            });
        }
    }

    // update buttons style
    function UpdateColumn(use_column, selected_use_level) {
        switch (selected_use_level) {
            case '0':
                // remove all fills
                $(use_column).children('button').addClass('use_level_button_0');
                break;
            case '1':
                // remove top 2
                $($(use_column).children('button')[0]).addClass('use_level_button_0');
                $($(use_column).children('button')[1]).addClass('use_level_button_0');
                $($(use_column).children('button')[2]).removeClass('use_level_button_0');
                break;
            case '2':
                // remove top 1
                $($(use_column).children('button')[0]).addClass('use_level_button_0');
                $($(use_column).children('button')[1]).removeClass('use_level_button_0');
                $($(use_column).children('button')[2]).removeClass('use_level_button_0');
                break;
            case '3':
                // show all fills
                $($(use_column).children('button')[0]).removeClass('use_level_button_0');
                $($(use_column).children('button')[1]).removeClass('use_level_button_0');
                $($(use_column).children('button')[2]).removeClass('use_level_button_0');
                break;
            case '4':
                // add "high level" style
                break;
        }
    } // end UpdateColumn

});
