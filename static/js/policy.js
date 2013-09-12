/*wait until document is loaded*/
//TODO need to fix how pdict for pwpolicy is passed/received from server; then check if summarizePolicy works

var pwpolicy;

/* attempt to move to knockout, in process
policyModel = {
    aut_num_optionValues : ["0", "1", "2"],
    aut_num_selectedOptionValue : ko.observable("0"),
    aut_num1_optionValues : ["none", "biometric", "passfaces", "password"],
    aut_num1_selectedOptionValue : ko.observable("none"),
    aut_num2_optionValues : ["none", "biometric", "passfaces", "password"],
    aut_num2_selectedOptionValue : ko.observable("none"),
    employee_SelectedOptionValue : ko.observable(),
    aut_num_function: function(option) {
           if(option=='0'){
                $("#aut_num1").hide();
                $("#aut_num2").hide();
                policyModel.aut_num1_selectedOptionValue("none");
                policyModel.aut_num2_selectedOptionValue("none");
                hide_policies();
                //remove all options
           }else if(option=='1'){
                $("#aut_num1").show();
                $("#aut_num2").hide();
                policyModel.aut_num2_selectedOptionValue("none");
           }else if(option=='2'){
                $("#aut_num1").show();
                $("#aut_num2").show();
           }
    },
    aut_function: function(option1,option2){
            if(option1=='none'&&option2=='none'){
                   hide_policies();
            }else if(option1==option2 && option1!='none'){
                   toastr['error']('Please, select two distinct options or change the number of mechanisms.');
                   policyModel.aut_num1_selectedOptionValue("none");
                   policyModel.aut_num2_selectedOptionValue("none");
                   hide_policies();
            }else{
                hide_policies();
                $("#"+option1+"_policy").show();
                $("#"+option2+"_policy").show();
            }
    }
};
ko.applyBindings(policyModel, document.getElementById('policy_form'));
*/
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
    $("#sets" + 1).prop('checked', true);
    $("#sets" + 1).change();
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

function displayContextualizedPolicy(contextualized) {
    var factorIdx = {"biometric": 0, "passfaces": 1, "password": 2};
    console.log('calling displayContex');
    console.log(contextualized);
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

    console.log('reached line');
    //console.log('length ' + factors.length);
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
    //displayContextualizedPolicy(window.last_found);
    //update_password_form(window.last_found);
    //update_biometric_form(window.last_found);
    //update_passfaces_form(window.last_found);
    updateScoreFrame();

    //console.log(policy['policy'][0]['employee'] + " " + policy['policy'][0]['location'] + " " + policy['policy'][0]['device']);
    // TODO: store all policies so that when user changes context (employee, location, device) checkboxes, different policies are visualized
    //displayContextualizedPolicy(policy['policy'][0]);
}

//3 different authentication mechanisms
    $('#aut_num').change(autNumChangeFunction);


    function autNumChangeFunction(){
    $("#authentication1").remove();
    $("#authentication2").remove();
    hide_policies();
    //remove all options
    //    <option value="" disabled selected>number</option>

    var options = ['none set',  // need to do -1 to get the rest of the values
                   'biometric',   //value:0
                   'passfaces/swipe-lock',                  //value:1
                   'passwords'];                            //value:2

    for (var i = 0; i < $('#aut_num').val(); i++) {  // use i+1, because indices in form start from 1
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

};
$(".aut").change(function(){
    if($('#aut_num').val()==2 && ($('#authentication1').val()==$('#authentication2').val())){ //ensure distinct selected options
        hide_policies();
        toastr['error']('Please, select two distinct options or change the number of mechanisms.');
    }else{
        display_policies();
    }
    submitAlternativesRequest();
})

function display_policies(){ //display selected policies only
    hide_policies();

    $('.policy' +$("#authentication1").val()).show();
    $('.policy' +$("#authentication2").val()).show();
}
function hide_policies(){ //hide all policies
    $('.policy').each(function(){
        $(this).hide();
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

function resetPolicyForm(){
        policies_array = {};
        $("#policy_form")[0].reset();
        $("#authentication1").remove();
        $("#authentication2").remove();
        hide_policies();
        clear_policy_summary();
        $('#chartContainer').empty();
}
//write policyUpdate array on apply btn press
$("#apply").click(function () {
    if (!policies_array.employee || !policies_array.location || !policies_array.device //if no employee/locn/device
        || $.isEmptyObject(policies_array.employee)
        || $.isEmptyObject(policies_array.location)
        || $.isEmptyObject(policies_array.device)) {
        policies_array.employee = ['executives', 'desk', 'road'];
        policies_array.location = ['office', 'public', 'home'];
        policies_array.device = ['desktop', 'laptop', 'phone'];
        //policyUpdate = policyUpdate.concat(policies_array);
        toastr['info']('You have not chosen any location, employee or device. All options will be selected');
    }
    if (!policies_array.policyDelta) {
        toastr['error']('Failed to apply policy. You have not chosen any number of the authentication mechanisms');
    } else {
        policyUpdate = policyUpdate.concat(policies_array);
        //reset policies form
        resetPolicyForm();
        console.log(policyUpdate);
        toastr['info']('Policy saved. All the changes will be applied in the end of the month. Once you have finished updating the policies, please press the play button to continue');
    }
});


$('.aut').change(function(){ //if one of the names of mechanism to be used was changed
    if($('.authentication').val()>=1){
            var policy1 = $('.policy' +$("#authentication1").val()).attr('id');
            //$('.policy' +$("#authentication1").val()).find('.target').change();
            summarizePolicy(policies_array);
            if($('.authentication').val()==2){
                var policy2 = $('.policy' +$("#authentication2").val()).attr('id'); //if exists
                //$('.policy' +$("#authentication2").val()).find('.target').change();
                summarizePolicy(policies_array);
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
     if (policy=='biometric'){
         policies_array.policyDelta[policy]['bdata']='0';
     }else if (policy=='passfaces'){
         policies_array.policyDelta[policy]['pdata']='0';
     }else if (policy=='pwpolicy'){
         policies_array.policyDelta[policy]['plen']='0';
     }

     $('#sum-'+policy).text('');
     if($('#aut_num').val()=='0'){
        policies_array.policyDelta.pwpolicy.plen= '0';
        policies_array.policyDelta.biometric.bdata= '0';
        policies_array.policyDelta.passfaces.pdata= '0';
     }
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
        //console.log('test');
        //console.log(policies_array['employee'][0]);
        //console.log(policies_array['location']);
        if (policies_array['location']!= undefined && policies_array['employee']!=undefined && policies_array['device']!=undefined)
        {
            if (policies_array['employee'].length!=0 && policies_array['location'].length!=0 && policies_array['device'].length!=0)
            {
                 var policy = find_policy(policies_array['employee'][0], policies_array['location'][0], policies_array['device'][0]);
                 //console.log('')
                 if(policy != {})
                 {
                  //displayContextualizedPolicy(window.last_found);
                  update_password_form(window.last_found);
                  update_biometric_form(window.last_found);
                  update_passfaces_form(window.last_found);
                      console.log('');
                      //piece of code for displaying the correspondong number and names of mechanisms
                      //accompanied with options for them
                      var mechanisms = get_factors(window.last_found);
                      var mechanisms_names = {"biometric": 0, "passfaces": 1, "password": 2};
                      $("#aut_num").val(mechanisms.length);
                      autNumChangeFunction();
                      for (var i = 0; (i < mechanisms.length) && (i < 2); i++) {
                            $("#authentication" + (i+1)).val(mechanisms_names[mechanisms[i]]);
                      }
                      hide_policies();
                      for (var k in mechanisms){
                            $('#'+mechanisms[k]+'_policy').show();    //display only active policies for the current combination of emp-dev-locn
                      }
                      //////////ended
                  }
             }
        }
        //update_password_form(policy);
       //
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
    console.log('target changed by ' + attribute);
    console.log(policies_array);
    summarizePolicy(policies_array);
    submitAlternativesRequest();
});

function find_policy(employee, location, device) {
    var tmp = {};
    console.log('looking for policy:' + employee + ' ' + location + ' ' + device);
    $(window.currentPolicy).each(function (policy_ind) {;
        console.log('current policy');
        console.log(window.currentPolicy[policy_ind]);
        if (window.currentPolicy[policy_ind]['employee'] == employee && window.currentPolicy[policy_ind]['location'] == location && window.currentPolicy[policy_ind]['device'] == device)
        {
            console.log('policy found');
            console.log(window.currentPolicy[policy_ind]);
            tmp = window.currentPolicy[policy_ind];
            window.last_found = window.currentPolicy[policy_ind];
            return tmp;
        }
    });
}