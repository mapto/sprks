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
var policyUpdate = [];
var policies_array = {};


function initFrame () {

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

    startTimer = function(interval) {
        console.log("timer started");
        //window.open("/incident","_self")
        if(window.timer1!=null) pauseInterval();
        window.timer1 = setInterval(function(){

            var tmp = new Date(window.date);
            var addHours = 24;
            var addDays = 1;

            //tmp.setDate(tmp.getDate()+addDays);
            tmp.setHours(tmp.getHours()+addHours);

            var new_date = tmp.getFullYear()+'-'+(tmp.getMonth()+1)+'-'+tmp.getDate();
            $('#time').text(new_date);
            window.date = new_date;
            check_events();
            if(window.date==window.nextSyncStr) {
                alert("Changes submitted");
                window.first_date = new Date(window.date);
                window.nextSync = window.first_date;
                window.nextSync.setMonth(window.nextSync.getMonth()+2);
                window.nextSync.setDate(1);
                window.nextSyncStr = window.nextSync.getFullYear()+'-'+window.nextSync.getMonth()+'-'+window.nextSync.getDate();
                submit_change();
            }
            },interval);
        return false;
    }

    pauseInterval = function() {
        clearInterval(window.timer1);
    }
    //function for sending request on play btn press
   // $('#play').click(send);

   // $('#play').click(startTimer);
    $('#pause').click(function() {
        $('.target').removeAttr('disabled');
        $('#apply').removeAttr('disabled');
        pauseInterval();

    });

    $('#forward').click(function() {
        $('.target').attr('disabled', 'disabled');
        $('#apply').attr('disabled', 'disabled');
        startTimer(500);
    })

    $('.target').change(function(){
        window.id_elem = $(this).closest($(".qn")).attr('id');
    })
    //$('#time').text("test");
    //opening incident window
    $('#play').click(function () {
        $('.target').attr('disabled', 'disabled');
        $('#apply').attr('disabled', 'disabled');
       // submit_change();
        startTimer(3000);
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
            css_class = "policy_btn";
    }

    $("." + css_class + " a").css("background-color", "#C10000");
    $("." + css_class + " a").css("color", "#fff");
    $("." + css_class + " a").css("cursor", "default");
}






//time-control buttons active css
$('#play').click(function() {
   $(this).parent().addClass('active');
   $('#pause').parent().removeClass('active');
   $('#forward').parent().removeClass('active');
});
$('#pause').click(function() {
   $(this).parent().addClass('active');
   $('#play').parent().removeClass('active');
   $('#forward').parent().removeClass('active');
});
$('#forward').click(function() {
   $(this).parent().addClass('active');
   $('#play').parent().removeClass('active');
   $('#pause').parent().removeClass('active');
});


//populate policies_array onchange of inputs
$('.target').bind("change", function(){
   var attribute = $(this).parent().attr('id'); //can be empployee/device/location/biometric/passfaces/plen/psets/etc.
   if(attribute=='employee'||attribute=='location'||attribute=='device'){   //write employee/location/device
       if(!policies_array[attribute]){          //if doesn't exist, initialize array
           policies_array[attribute]=[]
       }
       if($(this).prop('checked')){
           policies_array[attribute] = policies_array[attribute].concat($(this).val());
       }else{
           var index = policies_array[attribute].indexOf($(this).val());
           policies_array[attribute].splice(index, 1); //remove item from list if a checkbox has been unchecked
       }
   }else if(attribute=='policy_form'){ //if number of used mechanisms is changed
        //console.log($(this).val()+' policies'); //how many policies to be passed
        if (!policies_array.policyDelta){        //initialize dictionary if doesn't exist
           policies_array.policyDelta={};
        }
        null_unused_policy('biometric');
        null_unused_policy('passfaces');
        null_unused_policy('pwpolicy');
   }else{                                       //write the policyDelta
       if (!policies_array.policyDelta){        //initialize dictionary if doesn't exist
           policies_array.policyDelta={};
       }
       if(attribute=='biometric_policy' || attribute=='passfaces_policy'){
           policies_array.policyDelta[attribute.replace('_policy','')] = {};
           policies_array.policyDelta[attribute.replace('_policy','')][attribute.substring(0,1)+'data'] = $(this).val();
       }else{
           if(!policies_array.policyDelta.pwpolicy){
           policies_array.policyDelta.pwpolicy={};
           }
           policies_array.policyDelta.pwpolicy[attribute] = $(this).val();//write pwpolicy
       }
   }
   //console.log(policies_array);
});

$('.aut').change(function(){ //if one of the names of mechanism to be used was changed
    if($('.authentication').val()>=1){
            var policy1 = $('.policy' +$("#authentication1").val()).attr('id');
            if($('.authentication').val()==2){
                var policy2 = $('.policy' +$("#authentication2").val()).attr('id'); //if exists
            }
    }
    if(policy1!= 'biometric_policy' && policy2!= 'biometric_policy'){null_unused_policy('biometric');}
    if(policy1!= 'passfaces_policy' && policy2!= 'passfaces_policy'){null_unused_policy('passfaces');}
    if(policy1!= 'password_policy' && policy2!= 'password_policy'){null_unused_policy('pwpolicy');}
});

function null_unused_policy(policy){
     policies_array.policyDelta[policy]={};
}
//write policyUpdate array on apply btn press
$("#apply").click(function(){
    if(!policies_array.employee || !policies_array.location || !policies_array.device //if no employee/locn/device
        || $.isEmptyObject(policies_array.employee)
        || $.isEmptyObject(policies_array.location)
        || $.isEmptyObject(policies_array.device)){
        alert('Failed to apply policy. You have to check at least one of the employees, locations and devices');
    }else if(!policies_array.policyDelta){
        alert('Failed to apply policy. You have not chosen any number of the authentication mechanisms');
    }else{
        policyUpdate = policyUpdate.concat(policies_array);
        //reset policies form
        policies_array = {};
        $("#policy_form")[0].reset();
        $("#authentication1").remove();
        $("#authentication2").remove();
        hide_policies();
        console.log(policyUpdate);
        alert('Policy saved. All the changes will be applied in the end of the term. Once you have finished updating the policies, please press the play button to continue')
    }
});

