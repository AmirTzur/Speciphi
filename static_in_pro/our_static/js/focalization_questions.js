$(document).ready(function () {
    // show first question
    $('div.questions').first().children('div.question').first().css('display', 'inline-block');
    // prevent default button action
    $('button.answer').click(function (event) {
        event.preventDefault();
        // sent taltul question and answer id using ajax
    });
    // show questions according to select chose
    $('select').on('change', function () {
        $('div.question').css('display', 'none');
        $('div#questions_' + this.value + ' div:nth-child(1)').css('display', 'inline-block');
    });

});