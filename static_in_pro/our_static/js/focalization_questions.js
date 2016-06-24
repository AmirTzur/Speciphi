$(document).ready(function () {
    var desktop_flag = false;

    // show and save first question
    $('div.questions').first().children('div.question').first().css('display', 'inline-block');
    var $current_question = $('div.questions').first().children('div.question').first();
    // show question indicator
    $current_question.parent('div.questions').children('div.question').each(function (index) {
        $('#question_indicators div:nth-child(' + parseInt(index + 1) + ')').css('display', 'inline-block');
    });

    // button clicks bind
    // prevent form submission
    $('button.answer').on('click', PD);
    // increase / decrease subject and option number and style button
    $('button.answer').on('click', AnswerClick);
    // IMPLEMENT: sent taltul question and answer id using ajax

    // display questions according to select chose
    $('select').on('change', function () {
        $('div.question').css('display', 'none');
        // var display_question = $('#questions_list').find(":selected").text()[1];
        // display first question and update current question
        $current_question = $('div#questions_' + this.value + ' div.question:nth-child(1)').css('display', 'inline-block');
        // hide last question indicator
        $('.question_indicator').css('display', 'none');
        $('#question_indicators').children('div.indicator_on').removeClass('indicator_on');
        // show current question indicator
        $current_question.parent('div.questions').children('div.question').each(function (index) {
            $('#question_indicators div:nth-child(' + parseInt(index + 1) + ')').css('display', 'inline-block');
        });
        // fill first indicator
        $('#question_indicators div.question_indicator:nth-child(1)').addClass('indicator_on');
    });

    // forward to next questions
    $('#question_nav_right').on('click', function () {
        if ($current_question.next('div').length) {
            $current_question.css('display', 'none');
            $current_question.next('div').css('display', 'inline-block');
            // update current question
            $current_question = $current_question.next('div');
            // update question indicator
            $('div#question_indicators').children('div.indicator_on').removeClass('indicator_on').next('div.question_indicator').addClass('indicator_on');
        }
    });

    // backward to last question
    $('#question_nav_left').on('click', function () {
        if ($current_question.prev('div').length) {
            $current_question.css('display', 'none');
            $current_question.prev('div').css('display', 'inline-block');
            // update current question
            $current_question = $current_question.prev('div');
            // update question indicator
            $('div#question_indicators').children('div.indicator_on').removeClass('indicator_on').prev('div.question_indicator').addClass('indicator_on');

        }
    });

    // responsive query
    function WidthChange() {
        // mobile screens
        if (window.matchMedia("(max-width: 991px)").matches) {
            // if was on desktop
            if (desktop_flag) {
                // display only 1 question
                $current_question.siblings('div.question').css('display', 'none');
                // select last displayed questions
                $("select#questions_list").val($current_question.parent('div.questions').prop('id').substring('questions_'.length));
                // remove side question style
                $('div.question').removeClass('side_question');
                $('div.answers').css('display', '');
                $('button.answer').css('display', '');
                $('div.questions').css('marginLeft', '');
            }
            desktop_flag = false;
        } //end mobile screens
        // desktop screens
        else if (window.matchMedia("(min-width: 992px)").matches) {
            desktop_flag = true;

            // on first desktop entry
            if (!$('#desktop_questions_list').length) {
                // create questions row container
                $('#questions_list').before(
                    "<div id='desktop_questions_list' class='row'>" +
                    "</div>"
                );
                // add elements to questions container
                $('select#questions_list').children('option').each(function () {
                    $('div#desktop_questions_list').append(
                        "<div id='questions_desktop_container_" + $(this).attr('value') + "' class='questions_desktop_container' style='display: inline-block'>" +
                        "<span class='questions_subject' style='display: block;'>" + $(this).attr('data-brand') +
                        "</span>" +
                        "<button id='questions_circle_" + $(this).attr('value') + "' class='questions_circle' style='display: block;'>" +
                        $(this).text()[1] + $(this).text()[2] + $(this).text()[3] +
                        "</button>" +
                        "</div>"
                    )
                });

                // prevent questions circle action
                $('button.questions_circle').on('click', PD);

                // display pressed subject questions (only if user didn't press on displayed subject)
                $('div.questions_desktop_container').on('click', function () {
                    var pressed_subject_id = $(this).children('button').prop('id').substring('questions_circle_'.length);
                    var displayed_subject_id = $current_question.parent('div').attr('id').substring('questions_'.length);
                    if (pressed_subject_id != displayed_subject_id) {
                        $('div.question').css('display', 'none');
                        $('div#questions_' + pressed_subject_id + ' div.question').css('display', 'inline-block');
                        // update current question
                        $current_question = $('div#questions_' + pressed_subject_id).children('div.question').first();
                        StyleQuestions($current_question);
                        UpdateDisplaySubject($current_question);
                    }
                });
                // add line separator
                $('div#questions_holder').before('<hr id="line_separator"/>');

                // add questions subject display
                $('hr#line_separator').before(
                    "<div id='questions_desktop_container_display'>" +
                    "<span id='questions_subject_display' style='display: block;'>" +
                    "</span>" +
                    "<div id='questions_circle_display' style='display: block;'>" +
                    "</div>" +
                    "</div>"
                );

                // switch to side question
                $(document).on('click', '.side_question', function () {
                    // switch sides
                    if ($(this).next('div.question').length) {
                        $(this).insertAfter($(this).next('div.question'));
                        StyleQuestions($(this).prev());
                    } else if ($(this).prev('div.question').length) {
                        $(this).insertBefore($(this).prev('div.question'));
                        StyleQuestions($(this).next());
                    }
                    UnStyleQuestion($(this));
                });

            } // end first desktop entry

            // show current question brothers
            $current_question.parent('div.questions').children('div.question').css('display', 'inline-block');
            StyleQuestions($current_question);

            // fill displayed subject content
            UpdateDisplaySubject($current_question);

            // update number of answered questions (from mobile select box)
            $('select#questions_list').children('option').each(function () {
                $('button#questions_circle_' + $(this).val()).text($(this).text()[1] + $(this).text()[2] + $(this).text()[3]);
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

    function UpdateAnsweredNumber($subject, increase, mobile) {
        var inner_text = $subject.text();
        if (mobile) {
            if (increase) {
                // get text of current questions subject (select option)
                switch (inner_text[1]) {
                    case '0':
                        inner_text = String(inner_text).replace('(0', '(1');
                        break;
                    case '1':
                        inner_text = String(inner_text).replace('(1', '(2');
                        break;
                    case '2':
                        inner_text = String(inner_text).replace('(2', '(3');
                        break;
                    case '3':
                        inner_text = String(inner_text).replace('(3', '(4');
                        break;
                }
            } else {
                switch (inner_text[1]) {
                    case '1':
                        inner_text = String(inner_text).replace('(1', '(0');
                        break;
                    case '2':
                        inner_text = String(inner_text).replace('(2', '(1');
                        break;
                    case '3':
                        inner_text = String(inner_text).replace('(3', '(2');
                        break;
                    case '4':
                        inner_text = String(inner_text).replace('(4', '(3');
                        break;
                }
            }
        } else {
            // desktop
            if (increase) {
                // get text of current questions subject (select option)
                switch (inner_text[0]) {
                    case '0':
                        inner_text = String(inner_text).replace('0/', '1/');
                        break;
                    case '1':
                        inner_text = String(inner_text).replace('1/', '2/');
                        break;
                    case '2':
                        inner_text = String(inner_text).replace('2/', '3/');
                        break;
                    case '3':
                        inner_text = String(inner_text).replace('3/', '4/');
                        break;
                }
            } else {
                switch (inner_text[0]) {
                    case '1':
                        inner_text = String(inner_text).replace('1/', '0/');
                        break;
                    case '2':
                        inner_text = String(inner_text).replace('2/', '1/');
                        break;
                    case '3':
                        inner_text = String(inner_text).replace('3/', '2/');
                        break;
                    case '4':
                        inner_text = String(inner_text).replace('4/', '3/');
                        break;
                }
            }
        }
        $subject.text(inner_text);
    }

    function StyleQuestions($current) {
        // if 1 questions - normal
        // if 2 questions - 1st-cutted, 2nd-normal
        // if 3 questions - 1st-cutted, 2nd-normal, 3rd-cutted
        var $questions = $($current.parent('div.questions')).children('div.question');
        switch ($questions.length) {
            case 2:
                // style first question
                StyleQuestion($questions.first());
                // center second question
                $questions.parent().css('marginLeft', '');
                $questions.parent().css('marginLeft', '-=215px');
                break;
            case 3:
                $('div.questions').css('marginLeft', '');
                // style first question
                StyleQuestion($questions.first());
                // style last question
                StyleQuestion($questions.last());
                break;
            default:
                $('div.questions').css('marginLeft', '');
                break;
        }

        function StyleQuestion($question) {
            $question.addClass('side_question');
            $question.children('div.answers').addClass('side_answers');
            // if question was answered - show only answer and disable button click
            var hided_siblings = false;
            $($question.children('div.answers')).children('button').each(function () {
                if ($(this).attr('value') == '1') {
                    // hide brothers
                    $(this).siblings('button').css('display', 'none');
                    hided_siblings = true;
                }
            });
            // disable buttons click
            $($question.children('div.answers')).children('button.answer').off('click', AnswerClick);
            // question wasn't answered - hide all answers
            if (!hided_siblings) {
                $question.children('div.answers').css('display', 'none');
            }
        }
    }

    function UnStyleQuestion($question) {
        $question.removeClass('side_question');
        $($question.children('div.answers')).removeClass('side_answers');
        // bind answer button functionality
        $($question.children('div.answers')).children('button.answer').on('click', AnswerClick);
        // show all answers
        $question.children('div.answers').css('display', '');
        $($question.children('div.answers')).children('button.answer').css('display', '');
    }

    function UpdateDisplaySubject($current) {
        var subject_text = $('div#questions_desktop_container_' + $current.parent('div.questions').prop('id').substring('questions_'.length)).children('span').text();
        $('span#questions_subject_display').text(subject_text);
        var subject_answered = $('button#questions_circle_' + $current.parent('div.questions').prop('id').substring('questions_'.length)).text();
        $('div#questions_circle_display').text(subject_answered);
    }

    function PD(event) {
        event.preventDefault();
    }

    function AnswerClick() {
        console.log($(this).val());
        var $button = $(this);
        // if not selected before - increase select box number of questions answered
        var increase_answered = true;
        $($button.parent('div.answers')).children('button.answer').each(function () {
            // if already selected
            if ($(this).attr('value') == '1') {
                increase_answered = false;
            }
        });
        // update button pressed indicator
        // color 'on & off' state
        if ($button.attr('value') == '0') {
            // cancel selected brothers and color them 'off'
            $button.siblings('button').attr('value', '0');
            $button.siblings('button').css({
                'background-color': 'rgb(240, 240, 240)',
                'font-weight': 'normal'
            });
            // check and color 'on'
            $button.attr('value', '1');
            $button.css({
                'background-color': 'rgb(220, 220, 220)',
                'font-weight': 'bold'
            });
        }
        else if ($button.attr('value') == '1') {
            // un check and color 'off'
            $button.attr('value', '0');
            $button.css({
                'background-color': 'rgb(240, 240, 240)',
                'font-weight': 'normal'
            });
        }

        // if no selection at the end - reduce at select box the number of questions answered
        var decrease_answered = true;
        $($button.parent('div.answers')).children('button.answer').each(function () {
            if ($(this).attr('value') == '1') {
                decrease_answered = false;
            }
        });

        // update questions number on select box
        if (increase_answered || decrease_answered) {
            var $current_subject = $('select#questions_list option[value=' + $current_question.parent('div').prop('id').substring('questions_'.length) + ']');
            UpdateAnsweredNumber($current_subject, increase_answered, true);
            if (window.matchMedia("(min-width: 992px)").matches) {
                $current_subject = $('button#questions_circle_' + $current_question.parent('div').prop('id').substring('questions_'.length));
                UpdateAnsweredNumber($current_subject, increase_answered, false);
                UpdateDisplaySubject($current_question);
            }
        }
    }

});