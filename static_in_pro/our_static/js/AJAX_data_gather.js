// affiliation
$('#nl-type-field input').on('change', function () {
    AJAX_userAction(this, 'affiliation_choosing');
});
// application
$('#nl-needs-field input').on('change', function () {
    AJAX_userAction(this, 'use_ranking');
});
// focalization
$('#nl-questions-field input').on('change', function () {
    AJAX_userAction(this, 'question_answering');
});
$('#info-elements button').on('click',function () {
    AJAX_userAction(this, 'advice_clicking');
});
// continue implementing closing advise and browsing advices

function AJAX_userAction(object, action_name) {
    var action_type;
    var object_id;
    var action_content;
    if (action_name == 'affiliation_choosing') {
        if ($(object).is(':checked')) action_type = 1;
        else action_type = -1;
        object_id = $(object).val();
    } else if (action_name == 'use_ranking') {
        action_type = $(object).val();
        if (!$(object).is(':checked')) action_type = -action_type;
        object_id = $(object).prop('id').substr(0, $(object).prop('id').indexOf('_'));
    } else if (action_name == 'question_answering') {
        action_type = $(object).val().substr($(object).val().indexOf('_') + 1);
        if (!$(object).is(':checked')) action_type = -action_type;
        object_id = $(object).val().substr(0, $(object).val().indexOf('_'));
    } else if (action_name == 'advice_clicking') {
        action_type = 1; // opening advisor
        object_id = $(object).val();
    }
    // send AJAX post request to NewConsulteeAffiliation view
    $.ajax({
        url: '/user_actions/',
        type: 'POST',
        data: {
            action_name: action_name,
            action_type: action_type,
            object_id: object_id,
            action_content: action_content
        },
        // handle a successful response
        success: function (json) {
            // need to implement...
            // update_deals(json['total_results'], json['offers']);
            console.log('success'); // log the returned json to the console
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText, errmsg, err); // provide a bit more info about the error to the console
        }
    });
}