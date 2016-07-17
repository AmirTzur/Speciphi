/**

 */
$(document).ready(function(){
    // My specs button
    $('#my-specs-btn').on('click', function () {
        $('#my-specs-window').fadeIn(50);
    });
    // Close button  - my specs window
    $("#specs-close").on('click', function () {
       $('#my-specs-window').fadeOut(50);
    });

    // media query event handler
    if (matchMedia) {
        var mq_mobile = window.matchMedia("(max-width: 767px)");
        mq_mobile.addListener(WidthChange);
        WidthChange();
    }
});

function WidthChange() {
    if (window.matchMedia("(max-width: 767px)").matches) {
        mobile_selection();
    }else if (window.matchMedia("(min-width: 768px)").matches) {
        remove_selection();
    }
}

function mobile_selection() {
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
}

function remove_selection() {
    $("#results-headers button").unbind('click');
    $("#results-section .results-deal").css('display', 'inline-block');
    $("#results-headers button").css('color', 'rgb(60, 65, 68)');
}