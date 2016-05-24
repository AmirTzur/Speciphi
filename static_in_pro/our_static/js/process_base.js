/**

 */

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
                // console.log(json); // log the returned json to the console
                update_deals(json['total_results'], json['offers']);
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText, errmsg, err); // provide a bit more info about the error to the console
            }
        });
}