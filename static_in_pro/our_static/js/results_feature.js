/**

 */

$(document).ready(function(){
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

    
});

function update_deals(total_results, offers) {
    console.log(total_results);
    // update total results
    $('#total-results span:nth-child(1)').text(total_results);
    // update deals
    console.log(offers);
    $('#list-group-horizontal').children('a').each(function(){
        // change link: a (this) href attr
        // change details: <div>-><span> : deal.sort_indicator, deal.price, deal.brand, deal.model
        // change src: img deal.image_url
    });
}