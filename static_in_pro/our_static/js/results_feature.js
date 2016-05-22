/**

 */

$(document).ready(function(){
    // Price Slider (jQuery UI)
    $(function() {
        $( "#slider-range" ).slider({
            range: true,
            min: 200,
            max: 10000,
            values: [200, 10000],
            disabled: false,
            slide: function(event, ui){
                $("#slider-min").val("$" + ui.values[0]);
                $("#slider-max").val("$" + ui.values[1]);
                console.log('slider moved');
            },
            stop: function(event, ui){
                alert('Define ajax callback to get results');
            },
        });
        $("#slider-min").val("$"+$("#slider-range").slider("values", 0));
        $("#slider-max").val("$"+$("#slider-range").slider("values", 1));
    });
    // Feature Open/Close Functionality
    $('#open-btn').click(function(){
        $('#close-mode').css('display', 'none');
        $('#open-mode').css('display', 'block');
        $('html, body').animate({scrollTop : $(document).height()},500);
    });
    $('#close-btn').click(function(){
        $('html, body').animate({scrollTop : 0},200, function(){
            $('#open-mode').css('display', 'none');
            $('#close-mode').css('display', 'block');
        });
    });
    
});

function update_deals(total_results, offers) {
    var deal, deal_offers;
    var deal_index = 0;
    // update total results
    $('#total-results span:nth-child(1)').text(total_results);
    // update deals details
    $('#deals-list a').each(function(){
        deal = offers[deal_index];
        deal_offers = deal["offers"];
        // change deal url
        $(this).attr('href', deal_offers[0]["deal_url"]);
        // change deal price
        $(this).find('.item-details span:nth-child(2)').text('$' + deal_offers[0]["price"]);
        // change deal brand and model
        $(this).find('.item-details span:nth-child(3)').text(deal["brand"] + ' ' + deal["model"]);
        // change deal image url
        $(this).find('img').attr('src', deal["image_url"]);
        deal_index += 1;
    });
}