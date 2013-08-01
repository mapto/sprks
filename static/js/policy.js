/*wait until document is loaded*/
//TODO need to fix how pdict for pwpolicy is passed/received from server; then check if summarize_policy works

var pwpolicy;

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

function updatePolicy(policy) {
    policyUpdate = [];
    statusReady();
    console.log('response from server:');
    console.log(policy);
    timelineModel.clockSpeed(0);
    timelineModel.currentDate(new Date(policy['date']));
    timelineModel.calendar(policy['calendar']);
    get_score_frame();

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

// used for horizontal buttons styling
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


//write policyUpdate array on apply btn press
$("#apply").click(function () {
    if (!policies_array.employee || !policies_array.location || !policies_array.device //if no employee/locn/device
        || $.isEmptyObject(policies_array.employee)
        || $.isEmptyObject(policies_array.location)
        || $.isEmptyObject(policies_array.device)) {
        toastr['error']('Failed to apply policy. You have to check at least one of the employees, locations and devices');
    } else if (!policies_array.policyDelta) {
        toastr['error']('Failed to apply policy. You have not chosen any number of the authentication mechanisms');
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
        toastr['info']('Policy saved. All the changes will be applied in the end of the term. Once you have finished updating the policies, please press the play button to continue');
    }

    submit_alternatives_request();

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


//populate policies_array onchange of inputs
$('.target').bind("change", function () {
    var attribute = $(this).parent().attr('id'); //can be empployee/device/location/biometric/passfaces/plen/psets/etc.
    if (attribute == 'employee' || attribute == 'location' || attribute == 'device') {   //write employee/location/device
        if (!policies_array[attribute]) {          //if doesn't exist, initialize array
            policies_array[attribute] = []
        }
        if ($(this).prop('checked')) {
            policies_array[attribute] = policies_array[attribute].concat($(this).val());
        } else {
            //console.log('unchecked');
            var index = policies_array[attribute].indexOf($(this).val());
            policies_array[attribute].splice(index, 1); //remove item from list if a checkbox has been unchecked
            //policies_array[attribute] = [];
        }
    } else if (attribute == 'policy_form') { //if number of used mechanisms is changed
        //console.log($(this).val()+' policies'); //how many policies to be passed
        if (!policies_array.policyDelta) {        //initialize dictionary if doesn't exist
            policies_array.policyDelta = {};
        }
        null_unused_policy('biometric');
        null_unused_policy('passfaces');
        null_unused_policy('pwpolicy');
    } else {                                       //write the policyDelta
        if (!policies_array.policyDelta) {        //initialize dictionary if doesn't exist
            policies_array.policyDelta = {};
        }
        //console.log($('#'+attribute).parent().attr('id'));      //can be biometric_policy or passsfaces_policy or password_policy
        if ($('#' + attribute).parent().attr('id') == 'biometric_policy' || $('#' + attribute).parent().attr('id') == 'passfaces_policy') {
            policies_array.policyDelta[$('#' + attribute).parent().attr('id').replace('_policy', '')] = {};
            policies_array.policyDelta[$('#' + attribute).parent().attr('id').replace('_policy', '')][$('#' + attribute).parent().attr('id').substring(0, 1) + 'data'] = $(this).val();
        } else {
            if (!policies_array.policyDelta.pwpolicy) {
                policies_array.policyDelta.pwpolicy = {};
            }
            if ($(this).prop('checked')) {
                policies_array.policyDelta.pwpolicy[attribute] = $(this).val();
            } else {
                //var index = policies_array.policyDelta.pwpolicy[attribute].indexOf($(this).val());
                policies_array.policyDelta.pwpolicy[attribute] = 0;

            }
            //policies_array.policyDelta.pwpolicy[attribute] = $(this).val();//write pwpolicy
        }
    }
    //console.log(policies_array);
    summarize_policy(policies_array);
});