/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 22/06/13
 * Time: 13:25
 * To change this template use File | Settings | File Templates.
 */
/*wait until document is loaded*/
//TODO need to fix how pdict for pwpolicy is passed/received from server; then check if summarize_policy works



var pwpolicy;

function initPolicy() {
    console.log('initPolicy called');

    console.log('starting to initialize sync date ')
    console.log(window.date);
    console.log(window.nextSyncStr);

    console.log("Policy initialized...");

    // defined in graphs.js
    // TODO should not handle the system event, because it is being used in automatic calls as well.
    // $('.target').change(submit_change_mul); //graphs are loaded if anything is changed
}

function verboseScore(score) {
    if (score < 0.2) {
        return "very low";
    }
    if (score < 0.4) {
        return "low";
    }
    if (score < 0.6) {
        return "average";
    }
    if (score < 0.8) {
        return "high";
    }
    if (score <= 1) {
        return "very high";
    }
}

function calculate_cost_from_calendar() {
    var tmp_calendar = window.calendar;
    var last_date = tmp_calendar.date;
    var tmp_prophecy = tmp_calendar.calendar;
    var sum = 0;
    $(tmp_prophecy).each(function(i) {
        if(tmp_prophecy[i].date < last_date)
        {

            var events = tmp_prophecy[i]._events;
            for(var j=0;j<events.length;j++)
            {
                sum+=events[j].cost;
            }
        }
    })
    return sum;
}

function get_factors(policy) {
    var factors = [];

//    {"bdata": 0, "pdata": 0, "plen": 0}
    if (policy['bdata'] && policy['bdata'] != 0) {
        factors.push('biometric');
    }
    if (policy['pdata'] && policy['pdata'] != 0) {
        factors.push('passfaces');
    }
    if (policy['plen'] && policy['plen'] != 0) {
        factors.push('password');
    }

    return factors;
}

function update_password_form(policy) {
    var plen = policy["plen"];
    //console.log("found plen " + plen);
    $("#len" + plen).prop("checked", true);
    $("#len" + plen).change();

    /*preset pswd sets value*/
    $("#sets" + policy["psets"]).prop('checked', true);
    $("#sets" + policy["psets"]).change();

    /*preset pswd dictionary value*/
    $("#dic").prop('checked', policy["pdict"] == 1);
    $("#dic").change();

    $("#hist" + policy["phist"]).prop('checked', true);
    $("#hist" + policy["phist"]).change();

    $("#renew" + policy["prenew"]).prop('checked', true);
    $("#renew" + policy["prenew"]).change();

    /*preset pswd attempts number check (yes/no)*/
    /* 0 - unlimited, 1 - limit of 10 attempts, 2 - limit of 3 attempts */
    $("#attempts" + policy["pattempts"]).prop('checked', true);
    $("#attempts" + policy["pattempts"]).change();

    /*preset pswd recovery option*/
    $("#recovery" + policy["precovery"]).prop('checked', true);
    $("#recovery" + policy["precovery"]).change();
}

function update_biometric_form(policy) {
    $("#biometric").val(policy["bdata"]);
    $("#biometric").change();

}

function update_passfaces_form(policy) {
    $("#passfaces").val(policy["pdata"]);
    $("#passfaces").change();
}

function display_contextualized_policy(contextualized) {
    var factorIdx = {"biometric": 0, "passfaces": 1, "password": 2};

    emp = contextualized['employee'];
    $("#" + emp).prop('checked', true);
    $("#" + emp).change();

    loc = contextualized['location'];
    $("#" + loc).prop('checked', true);
    $("#" + loc).change();

    dev = contextualized['device'];
    $("#" + dev).prop('checked', true);
    $("#" + dev).change();
    // TODO: handle policy for more than one environment (emp, loc, dev)

    factors = get_factors(contextualized);

    $("#aut_num").val(factors.length);
    $("#aut_num").change(); // have to do it manually, previous line doesn't call it

    for (var i = 0; (i < factors.length) && (i < 2); i++) {
        $("#authentication" + (i+1)).val(factorIdx[factors[i]]);
        $("#authentication" + (i+1)).change();

        // dynamically compose name of function and call it
        var fname = "update_" + factors[i] + "_form";  // compose function name
        window[fname](contextualized); // call function fname with parameter contextualized
    }

}

function update_policy(policy) {
    policyUpdate = [];
    statusReady();
    console.log('response from server:');
    console.log(policy);
    $('#pause').click();
    timelineModel.currentDate($.datepicker.parseDate($.datepicker.ISO_8601, policy['date']))
    window.date = $.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate);
    window.calendar = policy['calendar'];

    get_score_frame();

    setSyncDate();
    //console.log(policy['policy'][0]['employee'] + " " + policy['policy'][0]['location'] + " " + policy['policy'][0]['device']);
    // TODO: store all policies so that when user changes context (employee, location, device) checkboxes, different policies are visualized
    //display_contextualized_policy(policy['policy'][0]);
}

//3 different authentication mechanisms
$('#aut_num').change(function(){
    $("#authentication1").remove();
    $("#authentication2").remove();
    hide_policies();
    //remove all options
    //    <option value="" disabled selected>number</option>

    var options = ['none set',  // need to do -1 to get the rest of the values
                   'biometric',   //value:0
                   'passfaces/swipe-lock',                  //value:1
                   'passwords'];                            //value:2

    for (var i = 0; i < this.value; i++) {  // use i+1, because indices in form start from 1
        var s = $("<select class=\"target\" id=\"authentication" + (i+1) + "\" name=\"authentication" + (i+1) + "\" />");

        // Was previously for(var val in options)
        // It returned further values beyond the array items.
        // Probably these are the default attributes of a (dynamically created) object
        for(var val = 0; val < options.length; val++) {
            if (val == 0) {
                $("<option value=\"\" disabled selected>" + options[val] + "</option>").appendTo(s);
            } else {
                $("<option />", {value: val - 1, text: options[val]}).appendTo(s);
            }
        }
        s.appendTo("#aut" + (i+1));
        //create second options set
    }

});
$(".aut").change(function(){
    if($('#aut_num').val()==2 && ($('#authentication1').val()==$('#authentication2').val())){ //ensure distinct selected options
        hide_policies();
        toastr['error']('Please, select two distinct options or change the number of mechanisms.');
    }else{
        display_policies();
    }
})

function display_policies(){ //display selected policies only
    hide_policies();

    $('.policy' +$("#authentication1").val()).css("display","block");
    $('.policy' +$("#authentication2").val()).css("display","block");
}
function hide_policies(){ //hide all policies
    $('.policy').each(function(){
        $(this).css("display","none");
    });
}
function clear_policy_summary(){
    $('.policy-summary-field').each(function(){
        $(this).text('');
    });
}

$(function(){
    $('#employee').buttonset();
    $('#location').buttonset();
    $('#device').buttonset();

    $('#plen').buttonset();
    $('#psets').buttonset();
    $('#pdict').buttonset();
    $('#phist').buttonset();
    $('#prenew').buttonset();
    $('#pattempts').buttonset();
    $('#precovery').buttonset();
})
