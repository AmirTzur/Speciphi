/**

 */
// $(document).ready(function(){
//     var p_counter;
//     // Click event for information elements
//     $('#info-statistic').on('click', function () {
//         open_info(1,$('#statistic-text'), '#7ecad8', $('#info-statistic'));
//     });
//     $('#info-insight').on('click', function () {
//         open_info(2,$('#insight-text'), '#6ad874', $('#info-insight'));
//     });
//     $('#info-objective').on('click', function () {
//         open_info(3,$('#objective-text'), '#ab8eff', $('#info-objective'));
//     });
//     // Click event for close button
//     $('#info-close').on('click', function () {
//         $('#info-box').fadeOut(150);
//         // Delete all information <p>
//         $('#info-box .info-type:visible').empty('.box-text');
//     });
//     // Click event for pagination controllers
//     $('#info-pagination button:first-of-type').on('click', function () {
//         information_leafing(0);
//     });
//     $('#info-pagination button:last-of-type').on('click', function () {
//         information_leafing(1);
//     });
// });
//
// function open_info(nth_info, $info_div, info_color, $info_btn) {
//     // nth_info: 1=statistic ; 2=insight ; 3=objective
//     // Display information window
//     var p_counter = $info_div.children('p').length;
//     if (p_counter > 0) {
//         $('#info-box div').slice(1,4).hide();
//         $('#info-box div').slice(nth_info,nth_info+1).show();
//         $('#pagination-counter').text('1 / '+p_counter);
//         $info_div.children('p').hide();
//         $info_div.children(':first').show();
//         $('#info-box').css('background-color', info_color);
//         $('#info-box').fadeIn(150, function () {
//             // Zeroing info-button notification
//             $info_btn.find('span').text('');
//         });
//     }
// }
//
// function information_leafing(direction) {
//     // direction: 0=left/back ; 1=right/next
//     var $visible_div = $('#info-box .info-type:visible');
//     var p_counter = $visible_div.children('p').length;
//     var pagination_str = $('#pagination-counter').text();
//     var p_position = parseInt(pagination_str[0]);
//     if ( !((p_position == 1 && direction == 0) || (p_position == p_counter && direction == 1)) ){
//         var next_ind, $next_p;
//         // Choose the next or prev paragraph to show
//         $next_p = (direction == 1) ? $visible_div.children('p:visible').next('p') : $visible_div.children('p:visible').prev('p');
//         // Calculate pagination indicator
//         next_ind = (direction == 1) ? String((p_position % p_counter) + 1) : p_position - 1;
//         $visible_div.children('p:visible').hide();
//         $next_p.show();
//         // Update pagination indicator
//         $('#pagination-counter').text(next_ind + pagination_str.slice(1, pagination_str.length));
//     }
//
// }