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

    if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
        $(".risk-menu").css("display", "none");
    } else {
        $(".risk-menu").css("display", "block");
    }

    $(document).click(function () {
        if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
            $(".risk-menu").css("display", "none");
        } else {
            $(".risk-menu").css("display", "block");
        }
    });

    manageScoreIncidentButtons();


    send = function () {
        $("#curr_date").text('to be defined by server');
        var obj = {};
        var request = $.ajax({
            url: "/forward",
            type: "POST",
            data: JSON.stringify(obj),
            dataType: "json",
            success: function (curr_date) {
                console.log("success: " + JSON.stringify(curr_date));
                $("#curr_date").text(curr_date[0].value);
                manageScoreIncidentButtons();

            },
            error: function (response) {
                console.log("fail: " + response.responseText);
            }
        });
        return false;
    }




    //function for sending request on play btn press



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
    $('#play').click(function () {
        $('.target').attr('disabled', 'disabled');
        $('#apply').attr('disabled', 'disabled');
        startTimer(3000);
    });

    console.log("Private decoration initialized...");
}

// Decides whether to show score button
// If different elements of the interface need to show up in later turns,
// this could be done here


function manageScoreIncidentButtons() {
    if(time_parser($('#time').text())){
        var cur_date_greater = (new Date(time_parser($('#time').text())) - new Date('2014-2-1'));
        if(cur_date_greater<0){
                //console.log('less than 1 month passed. Score is not yet calculated, hide button');
                $(".score_page").css("display", "none");
        } else {
                //console.log('>=1 month passed. Score is calculated, show button.');
                $(".score_page").css("display", "block");
        }
    }

     $(".incident_page").css("display", "none");
}

// highlight active button(scores/story/policy)
function highlightActiveButton() {
    styles = {"background-color": "#C10000", "color": "#fff", "cursor": "default" };

    switch (title) {
        case "score":
            if($(".score_page").css("display")=== "block"){ css_class = "score";}
            break;
        case "intro":
            css_class = "intro";
            break;
        case "profile":
            css_class = "profile";
            break;
        case "incident":
            if($(".incident_page").css("display")=== "block"){ css_class = "incident";}
            break;
        case "policy":
            css_class = "policy";
            break;
        default:
            css_class = "";
    }

    deactivateButtons();

    $("." + css_class + "_page").css("background-color", "#C10000");
    $("." + css_class + "_page").css("color", "#fff");
    $("." + css_class + "_page").css("cursor", "default");


}

function deactivateButtons(){
    $('.intro_page').removeAttr('style');
    if($(".score_page").css("display")=== "block"){$('.score_page').removeAttr('style');}
    if($(".incident_page").css("display")=== "block"){$('.incident_page').removeAttr('style');}
    $('.profile_page').removeAttr('style');
    $('.policy_page').removeAttr('style');
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
       //console.log($('#'+attribute).parent().attr('id'));      //can be biometric_policy or passsfaces_policy or password_policy
       if($('#'+attribute).parent().attr('id')=='biometric_policy' || $('#'+attribute).parent().attr('id')=='passfaces_policy'){
           policies_array.policyDelta[$('#'+attribute).parent().attr('id').replace('_policy','')] = {};
           policies_array.policyDelta[$('#'+attribute).parent().attr('id').replace('_policy','')][$('#'+attribute).parent().attr('id').substring(0,1)+'data'] = $(this).val();
       }else{
           if(!policies_array.policyDelta.pwpolicy){
           policies_array.policyDelta.pwpolicy={};
           }
           policies_array.policyDelta.pwpolicy[attribute] = $(this).val();//write pwpolicy
       }
   }
   //console.log(policies_array);
    summarize_policy(policies_array);
});





$('.aut').change(function(){ //if one of the names of mechanism to be used was changed
    if($('.authentication').val()>=1){
            var policy1 = $('.policy' +$("#authentication1").val()).attr('id');
            //$('.policy' +$("#authentication1").val()).find('.target').change();
            summarize_policy(policies_array);
            if($('.authentication').val()==2){
                var policy2 = $('.policy' +$("#authentication2").val()).attr('id'); //if exists
                //$('.policy' +$("#authentication2").val()).find('.target').change();
                summarize_policy(policies_array);
            }
    }

    if(policy1!= 'biometric_policy' && policy2!= 'biometric_policy'){null_unused_policy('biometric');}
    if(policy1!= 'passfaces_policy' && policy2!= 'passfaces_policy'){null_unused_policy('passfaces');}
    if(policy1!= 'password_policy' && policy2!= 'password_policy'){null_unused_policy('pwpolicy');}
    policy1 = '';
    policy2 = '';

});

function null_unused_policy(policy){
     policies_array.policyDelta[policy]={};
     $('#sum-'+policy).text('');
}

//write policyUpdate array on apply btn press
$("#apply").click(function () {
    if (!policies_array.employee || !policies_array.location || !policies_array.device //if no employee/locn/device
        || $.isEmptyObject(policies_array.employee)
        || $.isEmptyObject(policies_array.location)
        || $.isEmptyObject(policies_array.device)) {
        manage_toast_alert('Failed to apply policy. You have to check at least one of the employees, locations and devices',3000);
    } else if (!policies_array.policyDelta) {
        manage_toast_alert('Failed to apply policy. You have not chosen any number of the authentication mechanisms',3000);
    } else {
        policyUpdate = policyUpdate.concat(policies_array);
        //reset policies form
        policies_array = {};
        $("#policy_form")[0].reset();
        $("#authentication1").remove();
        $("#authentication2").remove();
        hide_policies();
        clear_policy_summary();
        console.log(policyUpdate);
        manage_toast_alert('Policy saved. All the changes will be applied in the end of the term. Once you have finished updating the policies, please press the play button to continue',5000);
    }
});

function hideOtherPages(page_name) {
        $(".pages").each(function () {
            if ($(this).attr('id') !== page_name) {
                $(this).css("display", "none");
            }
        });
    }

function clearProfile() {
    $(".profile_table").each(function () {    //clear table
        this.remove();
    });
    $('#chartContainer').empty();           //clear graph

}

$('a').click('click', function () {
    var page = $(this).attr('class');
    if ((page.substr(page.length - 4)) === 'page') { //check if the link clicked if a page button
        hideOtherPages(page);

        $("#" + page).css("display", "block");
        if (page === 'policy_page') {
            initPolicy();
        }
        if (page === 'incident_page') {

        }
        if (page === 'profile_page') {
            clearProfile();
            initProfile();
        }
        if (page === 'score_page') {
            initScore();
        }

        title = page.substr(0, page.length - 5);
        highlightActiveButton();
        $(".main-body").css("display", "block");

        get_score_frame();
    }
});

$("#close_btn").click('click', function(){
    $(".main-body").css("display", "none");
    $(".pages").each(function(){
        $(this).css("display", "none");
    });
    deactivateButtons();
});

$(function () {
    if(getUsername()){resume()};

    if (getUserID() > 0) {
        $(".main-body").css("display", "block");
        $("#intro_page").css("display", "block");
        title = 'intro';
        highlightActiveButton();

        get_score_frame();
    } else {
        $(".main-body").css("display", "block");
        $("#home_page").css("display", "block");
    }

})