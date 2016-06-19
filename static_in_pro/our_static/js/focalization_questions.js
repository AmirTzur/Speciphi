$(document).ready(function () {
    // show and save first question
    $('div.questions').first().children('div.question').first().css('display', 'inline-block');
    var $current_question = $('div.questions').first().children('div.question').first();
    // prevent default button action
    $('button.answer').click(function (event) {
        event.preventDefault();
        // sent taltul question and answer id using ajax
    });
    // show questions according to select chose
    $('select').on('change', function () {
        $('div.question').css('display', 'none');
        $('div#questions_' + this.value + ' div:nth-child(1)').css('display', 'inline-block');
        // update current question
        $current_question = $('div#questions_' + this.value + ' div:nth-child(1)');
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