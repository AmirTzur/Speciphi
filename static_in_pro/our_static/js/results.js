/**

 */
$(document).ready(function(){
    // Results headers selection mechanism
    $("#results-headers button").each(function () {
        var sort_ind = parseInt($(this).attr('id').slice(-1))+1;
        $(this).on('click', function () {
            $("#results-headers button").css('color', 'rgb(60, 65, 68)');
            $(".results-deal").css('display', 'none');
            $(this).css('color', 'white');
            $("#results-section div:nth-of-type("+sort_ind+")").css('display', 'block');
        });
    });
    // Activate "Best Match" on load
    $("#results-headers button:nth-last-of-type(2)").click();

});