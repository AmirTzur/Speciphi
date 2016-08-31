// affiliation
$('.affiliation_input').on('change', function () {
    AJAX_userActionAffiliation(this);
});

function AJAX_userActionAffiliation(object) {
    var action_name = 'affiliation_choosing';
    var action_type;
    if ($(object).is(':checked')) action_type = 1;
    else action_type = -1;
    var object_id = $(object).val();
    var action_content;
    // send AJAX post request to NewConsulteeAffiliation view
    $.ajax({
        url: '/user_actions/', // the endpoint
        type: 'POST', // http method
        // data sent with the post request
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

// application
$('.application_input').on('change', function () {
    AJAX_userActionApplication(this);
});

function AJAX_userActionApplication(object) {
    var action_name = 'use_ranking';
    var action_type = $(object).val();
    if (!$(object).is(':checked')) action_type = -action_type;
    var object_id = $(object).prop('id').substr(0, $(object).prop('id').indexOf('_'));
    var action_content;
    // send AJAX post request to NewConsulteeAffiliation view
    $.ajax({
        url: '/user_actions/', // the endpoint
        type: 'POST', // http method
        // data sent with the post request
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

// focalization
$('.focalization_input').on('change', function () {
    AJAX_userActionFocalization(this);
});

function AJAX_userActionFocalization(object) {
    var action_name = 'question_answering';
    var action_type = $(object).val().substr($(object).val().indexOf('_') + 1);
    if (!$(object).is(':checked')) action_type = -action_type;
    var object_id = $(object).val().substr(0, $(object).val().indexOf('_'));
    var action_content;
    // send AJAX post request to NewConsulteeAffiliation view
    $.ajax({
        url: '/user_actions/', // the endpoint
        type: 'POST', // http method
        // data sent with the post request
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