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
// open info element
$('#info-elements button').on('click', function () {
    AJAX_userAction(this, 'advice_clicking');
});
// close info element
// $('#info-box button').on('click', function () {
//     AJAX_userAction(this, 'advice_clicking1');
// });
// continue implementing closing advise and browsing advices

function AJAX_userAction(object, action_name) {
    var action_type;
    var object_id;
    var action_content;
    // affiliation_choosing
    if (action_name == 'affiliation_choosing') {
        if ($(object).is(':checked')) action_type = 1;
        else action_type = -1;
        object_id = $(object).val();
        // use_ranking
    } else if (action_name == 'use_ranking') {
        action_type = $(object).val();
        if (!$(object).is(':checked')) action_type = -action_type;
        object_id = $(object).prop('id').substr(0, $(object).prop('id').indexOf('_'));
        // question_answering
    } else if (action_name == 'question_answering') {
        action_type = $(object).val().substr($(object).val().indexOf('_') + 1);
        if (!$(object).is(':checked')) action_type = -action_type;
        object_id = $(object).val().substr(0, $(object).val().indexOf('_'));
        // advice_clicking
    } else if (action_name == 'advice_clicking') {
        // open advisor
        if ($(object).parent().prop('id') == 'info-elements') {
            action_type = 1;
            object_id = $(object).val();
            console.log('open', object_id);
            // close advisor
        } else if ($(object).parent().prop('id') == 'info-close') {
            // not working!!!!
            // console.log('close');
            // action_type = -1;
            // object_id; // need to check which advise is it the we close
        }
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
            update_deals(json['offers']);
            console.log('success'); // log the returned json to the console
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText, errmsg, err); // provide a bit more info about the error to the console
        }
    });
}

function update_deals(offers) {

    $('#results-section .results-deal').each(function () {
        var sort_ind = $(this).attr('id');
        for (var i=0; i< offers.length; i++){
            if (offers[i]['sort_indicator'] == sort_ind){
                // ---Change deal <a> header---
                // image url
                $(this).children('a').children('img').attr('src', offers[i]['image_url']);
                // brand and line
                $(this).children('a').children('span').text(offers[i]['Brand'] + ' ' + offers[i]['Line']);
                // deal url
                $(this).children('a').attr('href', offers[i]['offers'][0]['deal_url']);
                // ---Change deal <div> drop down price---
                // deal url

                // ---Change deal <table> specification---
                var $specs_raw;
                var specs_index = 0;
                for(var feature_key in offers[i]['features']){
                    // get feature raw
                    $specs_raw = $(this).find('tbody').children('tr').eq(specs_index);
                    // change feature value name
                    if (feature_key != 'Storage'){
                        $specs_raw.children('td').eq(1).text(offers[i]['features'][feature_key]);
                    }else {
                        $specs_raw.children('td').eq(1).text(offers[i]['features'][feature_key][0]+' SSD\n'+offers[i]['features'][feature_key][1]+' HDD');
                    }
                    specs_index += 1;
                }
                // $(this).children('table tbody').each(function () {
                //
                // })
            }
        }
    });
    // var deal, deal_offers;
    // var deal_index = 0;
    // // update total results
    // $('#total-results span:nth-child(1)').text(total_results);
    // // update deals details
    // $('#deals-list a').each(function(){
    //     deal = offers[deal_index];
    //     deal_offers = deal["offers"];
    //     // change deal url
    //     $(this).attr('href', deal_offers[0]["deal_url"]);
    //     // change deal price
    //     $(this).find('.item-details span:nth-child(2)').text('$' + deal_offers[0]["price"]);
    //     // change deal brand and model
    //     $(this).find('.item-details span:nth-child(3)').text(deal["brand"] + ' ' + deal["model"]);
    //     // change deal image url
    //     $(this).find('img').attr('src', deal["image_url"]);
    //     deal_index += 1;
    // });
}
