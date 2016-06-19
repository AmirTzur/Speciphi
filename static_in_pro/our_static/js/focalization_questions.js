$(document).ready(function () {
    // show and save first question
    $('div.questions').first().children('div.question').first().css('display', 'inline-block');
    var $current_question = $('div.questions').first().children('div.question').first();
    // button's click
    $('button.answer').click(function (event) {
        // don't send form
        event.preventDefault();
        // update button pressed indicator
        // color 'on & off' state

        if ($(this).attr('value') == '0') {

            // cancel selected brothers and color them 'off'
            $(this).siblings('button').attr('value', '0');
            $(this).siblings('button').css('background-color', 'rgb(240, 240, 240)');
            // check and color 'on'
            $(this).attr('value', '1');
            $(this).css('background-color', 'rgb(220, 220, 220)');
        }
        else if ($(this).attr('value') == '1') {
            // un check and color 'off'
            $(this).attr('value', '0');
            $(this).css('background-color', 'rgb(240, 240, 240)');
        }
        // IMPLEMENT: sent taltul question and answer id using ajax
    });
    // display questions according to select chose
    $('select').on('change', function () {
        $('div.question').css('display', 'none');
        var display_question = $('#questions_list').find(":selected").text()[1];
        // display and update current question
        $current_question = $('div#questions_' + this.value + ' div.question:nth-child(' + display_question + ')').css('display', 'inline-block');
    });
    // forward to next questions
    $('#question_nav_right').on('click', function () {
        if ($current_question.next('div').length) {
            $current_question.css('display', 'none');
            $current_question.next('div').css('display', 'inline-block');
            // update questions number on select box
            $('select#questions_list').children('option').each(function () {
                if ('questions_' + $(this).prop('value') == $current_question.parent('div').prop('id')) {
                    var inner_text = $(this).text();
                    switch (inner_text[1]) {
                        case '1':
                            inner_text = String(inner_text).replace('(1', '(2');
                            break;
                        case '2':
                            inner_text = String(inner_text).replace('(2', '(3');
                            break;
                        case '3':
                            inner_text = String(inner_text).replace('(3', '(4');
                            break;
                        case '4':
                            inner_text = String(inner_text).replace('(3', '(4');
                            break;
                    }
                    $(this).text(inner_text);
                }
            });
            // update current question
            $current_question = $current_question.next('div');
        }
    });
    // backward to last question
    $('#question_nav_left').on('click', function () {
        if ($current_question.prev('div').length) {
            $current_question.css('display', 'none');
            $current_question.prev('div').css('display', 'inline-block');
            $('select#questions_list').children('option').each(function () {
                if ('questions_' + $(this).prop('value') == $current_question.parent('div').prop('id')) {
                    var inner_text = $(this).text();
                    switch (inner_text[1]) {
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
                    $(this).text(inner_text);
                }
            });
            // update current question
            $current_question = $current_question.prev('div');
        }
    });
});