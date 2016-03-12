function ShowEgg() {
    $('#menu1').css('display', 'inline');
    $('#drop_left').css('display', 'none');
    $('#drop_right').css('display', 'none');
}
function ShowEggs() {
    $('#menu1').css('display', 'none');
    $('#drop_left').css('display', 'inline');
    $('#drop_right').css('display', 'inline');

}

// media query change
function WidthChange(mq) {
    if (mq.matches) {//extra-small screens

        $('#right-side-nav').css('padding-left', '0px');

        //move dropdown2 to the right
        $('#myDropdown').css('right', '0px');

        /*locate dropdown2 vertically*/
        $('#myDropdown').css('top', '62px');

        //dropdown-eggs responsive behavioral
        if ($('.dropdown').hasClass('open')) {
            ShowEgg();
            $('#center-side-nav').css('padding-top', '8px');
        }
    }
    else {//small screens

        //give padding to right-side-nav to be the same width size as the left side nav
        //only on small screens and upper
        //example: if right=50px and left=100px, give right another 50px
        $('#right-side-nav').css('padding-left', parseInt($('#left-side-nav').css('width')) - parseInt($('#right-side-nav').css('width')) + 'px');

        //move dropdown2 to the right according to share elements width
        $('#myDropdown').css('right', '-' + (parseInt($('#share_icons').css('width')) + 5) + 'px');

        /*locate dropdown2 vertically*/
        $('#myDropdown').css('top', '37px');

        //dropdown-eggs responsive behavioral
        if ($('.dropdown').hasClass('open')) {
            ShowEggs();
            document.getElementById('drop_left').style.paddingRight = '108px';
        }
    }
}
// media query event handler
if (matchMedia) {
    var mq = window.matchMedia("(max-width: 767px)");
    mq.addListener(WidthChange);
    WidthChange(mq);
}

//show and hide eggs when user clicks on dropdown (only on small screens and higher)
$(document).ready(function () {
    $(".dropdown").on('show.bs.dropdown', function () {
        if (window.matchMedia("(min-width: 768px)").matches) {
            ShowEggs();
            document.getElementById('drop_left').style.paddingRight = '108px';
            $('#center-side-nav').css('padding-top', '12px');
        }
    });
    $(".dropdown").on('hide.bs.dropdown', function () {
        if (window.matchMedia("(min-width: 768px)").matches) {
            ShowEgg();
            $('#center-side-nav').css('padding-top', '8px');
        }
    });
});

//home orientation shape
document.getElementById("screens_holder").firstElementChild.firstElementChild.id = "square";

/* When the user clicks on the button,
 toggle between hiding and showing the dropdown content */
function opendrop2() {
    document.getElementById("myDropdown").classList.toggle("show");
}

//cancel iframe border
$('#accounts_iframe')[0].setAttribute('frameBorder','0');

////fix right-side-nav size according to register link text
//// media query change
//function WidthChange(mq) {
//    if (mq.matches) {
//        if ($('#register_links:first-child a').text() == 'Sign In') {
//            $('#right-side-nav').css('width', '148px');
//        } else if ($('#register_links:first-child a').text() == 'Sign Out') {
//            $('#right-side-nav').css('width', '160px');
//        }
//    }
//    else {
//        $('#right-side-nav').css('width', 'auto');
//    }
//}
//// media query event handler
//if (matchMedia) {
//    var mq = window.matchMedia("(min-width: 768px)");
//    mq.addListener(WidthChange);
//    WidthChange(mq);
//}


///* When the user clicks on the button,
// toggle between hiding and showing the dropdown content */
//function myFunction() {
//    document.getElementById("myDropdown").classList.toggle("show");
//}
//
//// Close the dropdown menu if the user clicks outside of it
//window.onclick = function (event) {
//    if (!event.target.matches('.dropbtn')) {
//        var dropdowns = document.getElementsByClassName("dropdown-content");
//        var i;
//        for (i = 0; i < dropdowns.length; i++) {
//            var openDropdown = dropdowns[i];
//            if (openDropdown.classList.contains('show')) {
//                openDropdown.classList.remove('show');
//            }
//        }
//    }
//}
