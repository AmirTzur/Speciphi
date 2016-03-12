/**
 Products Container Scripts
 */

$(document).ready(function () {
    //Temp fix for the dynamic gutters between the product divs
    $('#product-list').find('div').each(function () {
        $(this).insertAfter($("#product-list div:last-child"))
    });
    //Left control button: Click function
    $('#left-control-btn').click(function () {
        $("#product-list div:first-child").insertAfter($("#product-list div:last-child"));
    });
    //Right control button: Click function
    $('#right-control-btn').click(function () {
        $("#product-list div:last-child").insertBefore($("#product-list div:first-child"));
    });
});