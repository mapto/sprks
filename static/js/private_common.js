/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 21/06/13
 * Time: 16:18
 *
 * refactored so that calculations are not done both in Python and Javascript
 * In this case requested from the server and embedded in JS getters (Python, see html template) and calculated in client (JS, this file).
 *
 * this file works only with views/index_private.html because it relies on some webpy getter functions defined there
 */

function initFrame() {
    if ($("#risk").text() == '' || $("#cost").text() == '') {
        $(".risk-menu").css("display", "none");
    } else {
        $(".risk-menu").css("display", "block");
    }

    $(document).click(function () {
        if ($("#risk").text() == '' || $("#cost").text() == '') {
            $(".risk-menu").css("display", "none");
        } else {
            $(".risk-menu").css("display", "block");
        }
    });

//    manageScoreButton();

    manageButtons();


    send = function () {
        $("#curr_date").text('to be defined by server');
        var obj = {};
        var request = $.ajax({
            url: "/forward",
            type: "POST",
            async: false,
            data: JSON.stringify(obj),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (curr_date) {
                console.log("success: " + JSON.stringify(curr_date));
                $("#curr_date").text(curr_date[0].value);
                manageScoreButton();
                window.location.href = "/incident";
            },
            error: function (response) {
                console.log("fail: " + response.responseText);
            }
        });
        return false;
    }
    //function for sending request on play btn press
    $('.score').click(send);

    //opening incident window
    $('#play').click(function () {
        var width = 600;
        var height = 450;
        var left = (screen.width / 2) - (width / 2);
        var top = (screen.height / 2) - (height / 2);
        myWindow = window.open('/incident', 'incident', 'width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
        myWindow.focus();
    });

    console.log("Private decoration initialized...");
}

// Decides whether to show score button
// If different elements of the interface need to show up in later turns,
// this could be done here
function manageScoreButton() {
    if (isFirstTurn()) { // isFirstTurn() is defined in views/index_private.html template
        console.log('$content.date equal to start date. Don\'t show score.');
        $(".score").css("display", "none");
    } else {
        console.log('$content.date not equal to start date. Show score.');
        $(".score").css("display", "block");
    }
}

// highlight active button(scores/story/policy)
function manageButtons() {
    styles = {"background-color": "#C10000", "color": "#fff", "cursor": "default" };

    switch (contentTitle()) { // contentTitle() is defined in views/index_private.html template
        case "Scores":
            current_class = "score";
            hidden_class = "none";
            break;
        case "Introduction":
            current_class = "story";
            hidden_class = "score";
            $(".incident a").css("pointer-events", "none");
            $(".incident a").css("cursor", "default");
            $(".incident a").css("color", "#F2F2F2");
            break;
        case "Incident":
            current_class = "incident";
            hidden_class = "score";
            break;
        default:
            current_class = "policy";
            hidden_class = "score";
    }

    $("." + current_class + " a").css("background-color", "#C10000");
    $("." + current_class + " a").css("color", "#fff");
    $("." + current_class + " a").css("cursor", "default");

    $("." + hidden_class + " a").css("pointer-events", "none");
    $("." + hidden_class + " a").css("cursor", "default");
    $("." + hidden_class + " a").css("color", "#F2F2F2");
}
