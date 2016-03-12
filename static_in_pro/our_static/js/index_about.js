/**
 About Scripts
 */

$(document).ready(function () {
    //How it works - Mobile open/close
    $("#how-label").click(function () {
        if ($("#p-how-320").is(':hidden') && $("#p-how-768").css('display') == "none") {
            $(this).siblings().css('display', 'inline-block');
            $(this).css('font-size', '30px');
        }
        else if ($("#p-how-768").css('display') == "none") {
            $(this).siblings().css('display', 'none');
            $(this).css('font-size', '48px');
        }
    });
    //Who we are - Mobile open/close
    $("#who-we-label").click(function () {
        if ($("#p-who-we").is(':hidden') && $("#p-how-768").css('display') == "none") {
            $(this).siblings().css('display', 'inline-block');
            $(this).css('font-size', '30px');
        }
        else if ($("#p-how-768").css('display') == "none") {
            $(this).siblings().css('display', 'none');
            $(this).css('font-size', '48px');
        }
    });
    //How it works - Infographic Dynamic description text
    $("#info-stage1").click(function () {
        $("#desc-label-320").text("Pick a product");
        $("#desc-label-768").text("Pick a product");
        $("#desc-stage-320").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(1).");
        $("#desc-stage-768").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(1).");
        $("#infographic-line").nextUntil().css('border', 'none');
        $(this).css('border', 'dashed 1px #8c2b3d');
    });
    $("#info-stage2").click(function () {
        $("#desc-label-320").text("Stage 2");
        $("#desc-label-768").text("Stage 2");
        $("#desc-stage-320").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(2).");
        $("#desc-stage-768").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(2).");
        $("#infographic-line").nextUntil().css('border', 'none');
        $(this).css('border', 'dashed 1px #8c2b3d');
    });
    $("#info-stage3").click(function () {
        $("#desc-label-320").text("Stage 3");
        $("#desc-label-768").text("Stage 3");
        $("#desc-stage-320").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(3).");
        $("#desc-stage-768").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(3).");
        $("#infographic-line").nextUntil().css('border', 'none');
        $(this).css('border', 'dashed 1px #8c2b3d');
    });
    $("#info-stage4").click(function () {
        $("#desc-label-320").text("Stage 4");
        $("#desc-label-768").text("Stage 4");
        $("#desc-stage-320").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(4).");
        $("#desc-stage-768").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(4).");
        $("#infographic-line").nextUntil().css('border', 'none');
        $(this).css('border', 'dashed 1px #8c2b3d');
    });
    $("#info-stage5").click(function () {
        $("#desc-label-320").text("Stage 5");
        $("#desc-label-768").text("Stage 5");
        $("#desc-stage-320").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(5).");
        $("#desc-stage-768").text("" +
            "based on immaterial factors, rather than studying the indicators " +
            "that tell them whether they can make money(5).");
        $("#infographic-line").nextUntil().css('border', 'none');
        $(this).css('border', 'dashed 1px #8c2b3d');
    });
});