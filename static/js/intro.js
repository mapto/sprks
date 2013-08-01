$(function () {

    $("#interviewee1").on('click', function (e) {
        if ($("#quote1").css("display") == "block") {
            $("#quote1").hide();
        } else {
            $("#quote1").show();
            $("#quote2").hide();
            $("#quote3").hide();
            e.stopPropagation();
        }

    });
    $("#interviewee2").on('click', function (e) {
        if ($("#quote2").css("display") == "block") {
            $("#quote2").hide();
        } else {
            $("#quote2").show();
            $("#quote1").hide();
            $("#quote3").hide();
            e.stopPropagation();
        }
    });
    $("#interviewee3").on('click', function (e) {
        if ($("#quote3").css("display") == "block") {
            $("#quote3").hide();
        } else {
            $("#quote3").show();
            $("#quote2").hide();
            $("#quote1").hide();
            e.stopPropagation();
        }
    });

    $(document).click(function () {
        $("#quote1").hide();
        $("#quote2").hide();
        $("#quote3").hide();
    });

});
