/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 21/06/13
 * Time: 16:18
 *
 * refactored so that calculations are not done both in Python and Javascript
 * In this case requested from the server and embedded in JS getters (Python, see html template) and calculated in client (JS, this file).
 *
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



    manageScoreButton();
    manageIncidentButton();

    highlightActiveButton();


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
                manageIncidentButton();
            },
            error: function (response) {
                console.log("fail: " + response.responseText);
            }
        });
        return false;
    }

    startTimer = function() {
        console.log("timer started");
        //window.open("/incident","_self")
        window.timer1 = setInterval(function(){

            var tmp = new Date(window.date);
            var addHours = 24;
            tmp.setHours(tmp.getHours()+addHours);
            var new_date = tmp.getFullYear()+'/'+(tmp.getMonth()+1)+'/'+tmp.getDate();
            $('#time').text(new_date);
            window.date = new_date;
            check_events();
            },10000);
        return false;
    }

    pauseInterval = function() {
        clearInterval(window.timer1);
    }
    //function for sending request on play btn press
   // $('#play').click(send);

   // $('#play').click(startTimer);
    $('#pause').click(pauseInterval);
    //$('#time').text("test");
    //opening incident window
    $('#play').click(function () {
     //   submit_change();
        startTimer();
        //window.open("/incident","_self")
        //var width = 1000;
        //var height = 550;
        //var left = (screen.width / 2) - (width / 2);
        //var top = (screen.height / 2) - (height / 2);
        //myWindow = window.open('/incident', 'incident', 'width=' + width + ', height=' + height + ', top=' + top + ', left=' + left);
        //myWindow.focus();
    });

    console.log("Private decoration initialized...");
}

// Decides whether to show score button
// If different elements of the interface need to show up in later turns,
// this could be done here
function manageScoreButton() {
    if (false) { // originally tests for isFirstTurn() TODO
        console.log('$content.date equal to start date. Don\'t show score.');
        $(".score").css("display", "none");
    } else {
        console.log('$content.date not equal to start date. Show score.');
        $(".score").css("display", "block");
    }
}

function manageIncidentButton() {
/*
    var value = isFirstTurn() ? "none" : "block";
    console.log(".incident style is " + value);
    $(".incident").css("display", value);
*/
}

// highlight active button(scores/story/policy)
function highlightActiveButton() {
    styles = {"background-color": "#C10000", "color": "#fff", "cursor": "default" };

    switch (document.title) {
        case "Scores":
            css_class = "score";
            break;
        case "Introduction":
            css_class = "story";
            break;
        case "Profile":
            css_class = "profile";
            break;
        case "Incident":
            css_class = "incident";
            break;
        default:
            css_class = "policy";
    }

    $("." + css_class + " a").css("background-color", "#C10000");
    $("." + css_class + " a").css("color", "#fff");
    $("." + css_class + " a").css("cursor", "default");
}
