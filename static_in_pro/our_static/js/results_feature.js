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
