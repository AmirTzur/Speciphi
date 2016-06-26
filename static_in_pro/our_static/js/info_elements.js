/**

 */
$(document).ready(function(){
    $('#info-statistic').on('click', function () {
        open_info(0,$('#statistic-text'), '#7ecad8');
    });
    $('#info-insight').on('click', function () {
        open_info(1,$('#insight-text'), '#6ad874');
    });
    $('#info-objective').on('click', function () {
        open_info(2,$('#objective-text'), '#ab8eff');
    });
    $('#info-close').on('click', function () {
        $('#info-box').hide();
        //delete notification value from button
        //delete all <p> from div
        //add close event on screen click
    })
});


function open_info(nth_info, $info_div, info_color) {
    // nth_info: 1=statistic ; 2=insight ; 3=objective
    if ( $info_div.children('p').length > 0 ) {
        $('#info-box div').slice(0,3).hide();
        $('#info-box div').slice(nth_info,nth_info+1).show();
        $('#info-box').css('background-color', info_color);
        $('#info-box').show();
    }



}