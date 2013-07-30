/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 22/06/13
 * Time: 13:25
 * To change this template use File | Settings | File Templates.
 */
/*wait until document is loaded*/
var pwpolicy;

function initPolicy() {
    console.log('initPolicy called');

    console.log('starting to initialize sync date ')

    console.log(window.date);
    console.log(window.nextSyncStr);
    //submit_change();
   // $('.target').change(submit_change);
    //$('.target').change(submit_change_mul); //graphs are loaded if anything is changed

    //$('#play').click(send) // the play message is not sent from here, but from render decoration (views/index-private.html)

    var d = new Date();
    var strDate = d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear() + ", " + d.getHours() + ":" + d.getMinutes();

    //document.getElementById('curr_date').innerHTML = strDate;



    //if (!policyExists()) {
        // If code executed, then we have a new user
        // Greet them accordingly
    //    alert('This is your first visit. You can see the policy as it has been left by your predecessor.')
    //}

    // contains elements in the following order:



    console.log("Policy initialized...");

    //summarize_policy(pwpolicy); //update policy summary for user

    // defined in graphs.js
    // TODO should not handle the system event, because it is being used in automatic calls as well.
    // $('.target').change(submit_change_mul); //graphs are loaded if anything is changed
    //submit_change_mul();

}

function setSyncDate() {
    window.first_date = new Date(window.date);
    window.nextSync = window.first_date;
    window.nextSync.setMonth(window.nextSync.getMonth()+1);
    window.nextSync.setDate(1);
    window.nextSyncStr = window.nextSync.getFullYear()+'-'+(window.nextSync.getMonth()+1)+'-'+window.nextSync.getDate();
    window.id_elem = 'plen';
}

/****************UNCOMMENT if policy is initialised in a separate request
function getInitPolicy(){
    var msg = {};
    msg.initPolicy = true;
    console.log(msg);
    var request = $.ajax({
        url: "/api/chronos/sync",
        type: "POST",
        async: false,
        data: JSON.stringify(msg),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success : function(data) {
            pwpolicy = JSON.parse(data);
            console.log(pwpolicy);
            //$('#time').text(pwpolicy.date);
        },
        error: function(response) {
            console.log("failed getInitPolicy: " + response.responseText);
        }
    });
    return false;
}

*/

/* deprecated methos for getting initial policy
function getInitPolicy(){
    var request = jQuery.ajax({
        url: "/pwpolicy_rest",
        type: "GET",
        async:false,
        success : function(data) {
            pwpolicy = JSON.parse(data);
            console.log(pwpolicy);
            $('#time').text(pwpolicy.date);
        },
        error: function(response) {
            console.log("failed getInitPolicy: " + response.responseText);
        }
    });
    return false;
}
*/


function policyExists() {
        if (pwpolicy.notfound != 1){
            return true; // This value is set server-side
        }
        else {
            return false; // This value is set server-side
        }
}

function summarize_policy(policy){ //not currently used
    for (var key in policy){
        console.log(policy);
      // NEED TO FIX PDICT UNDEFINED

        if (policy[key]==''){alert('need to fix pdict');policy[key]=0;}
        $("#sum-"+key).text(key+' '+policy[key]);
    }
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

/* handle AJAX (realtime) submission */
/*
//sends data when users press play button
*/

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

function check_events() {
    var tmp_events_calendar = window.calendar;
    $(tmp_events_calendar).each(function(i) {
        var conv_date = new Date(tmp_events_calendar[i].date);
        var str_date = conv_date.getFullYear()+'-'+(conv_date.getMonth()+1)+'-'+conv_date.getDate();
        if(str_date == window.date)
        {
            $('#pause').click();
            tmp_event = tmp_events_calendar[i].events
            $(tmp_event).each(function(j){
                //alert("Event #"+tmp_event[j].incdt_id+" happend!");
                display_event(tmp_event[j].incdt_id, tmp_event[j].cost);
                submit_event(str_date);
            })
                $('.incident_page').click();

        }

    })

}

function submit_event(date){
        msg = {};
        msg['date'] = date;
        var request = $.ajax({
        url: "/api/chronos/event",
        type: "POST",
        // Async was false, but want to avoid perceived freeze on client side. Any risks, related to that?
        // E.g. what happens if the user changes screens too often
        async: true,
        data: JSON.stringify(msg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: function (response) {
            //
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
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
    console.log("found plen " + plen);
    $("#len" + plen).prop("checked", true);
    $("#len" + plen).change();

    // TODO: implement (copy from other place) other pwpolicy items
    /*preset pswd sets value*/
    console.log("found sets " + policy["psets"]);
    $("#sets" + policy["psets"]).prop('checked', true);
    $("#sets" + policy["psets"]).change();

    /*preset pswd dictionary value*/
    console.log("found " + (policy["pdict"] ? "use" : "no") + " dict");
    $("#dic").prop('checked', policy["pdict"] == 1);
    $("#dic").change();

    console.log("found phist difficulty " + policy["phist"]);
    $("#hist" + policy["phist"]).prop('checked', true);
    $("#hist" + policy["phist"]).change();

    console.log("found renew " + policy["prenew"]);
    $("#renew" + policy["prenew"]).prop('checked', true);
    $("#renew" + policy["prenew"]).change();

    /*preset pswd attempts number check (yes/no)*/
    /* 0 - unlimited, 1 - limit of 10 attempts, 2 - limit of 3 attempts */
    console.log("found attempts " + policy["pattempts"]);
    $("#attempts" + policy["pattempts"]).prop('checked', true);
    $("#attempts" + policy["pattempts"]).change();

    /*preset pswd recovery option*/
    console.log("found precovery " + policy["precovery"]);
    $("#recovery" + policy["precovery"]).prop('checked', true);
    $("#recovery" + policy["precovery"]).change();
}

function update_biometric_form(policy) {
    $("#biometric").val(policy["bdata"]);
}

function update_passfaces_form(policy) {
    $("#passfaces").val(policy["pdata"]);
}

function display_contextualized_policy(contextualized) {
    var factorIdx = {"biometric": 0, "passfaces": 1, "password": 2};

    emp = contextualized['employee'];
    // TODO; possibly uncheck all the rest. make class location and before setting next line unset all from class
    $("#" + emp).prop('checked', true);
    $("#" + emp).change();

    loc = contextualized['location'];
    // TODO; possibly uncheck all the rest. make class location and before setting next line unset all from class
    $("#" + loc).prop('checked', true);
    $("#" + loc).change();

    dev = contextualized['device'];
    // TODO; possibly uncheck all the rest. make class location and before setting next line unset all from class
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
        console.log(fname);
        window[fname](contextualized); // call function fname with parameter contextualized
    }

}

function update_policy(policy) {
    policyUpdate = [];
    statusReady();
    console.log('response from server:');
    console.log(policy);
    $('#pause').click();
    $('#time').text(time_visualiser(policy['date'], true));
    window.date = time_parser($('#time').text());
    window.calendar = policy['calendar'];

    manageScoreButton();
    get_score_frame();

    setSyncDate();
    //console.log(policy['policy'][0]['employee'] + " " + policy['policy'][0]['location'] + " " + policy['policy'][0]['device']);
    // TODO: store all policies so that when user changes context (employee, location, device) checkboxes, different policies are visualized
    //display_contextualized_policy(policy['policy'][0]);
}

function submit_change() { // need different event handling, to capture any change
    var msg = {
        date: time_parser($('#time').text()),
        policyUpdate: []
    };
    if(policyUpdate.length>0){
        msg.policyUpdate = policyUpdate;
        //msg.newCosts = calculate_cost_from_calendar();
    }
    msg.initPolicy = true;
    console.log(msg);
    statusUpdating();
    var request = $.ajax({
        url: "/api/chronos/update",
        type: "POST",
        data: JSON.stringify(msg),
        success: update_policy,
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function resume() {
    statusUpdating();
    var request = $.ajax({
        url: "/api/chronos/resume",
        type: "GET",
        success: function(policy) {
            policyUpdate = [];
            statusReady();
            console.log('response from server:' + policy);
            $('#pause').click();
            $('#time').text(time_visualiser(policy['date'], true));
            manageScoreButton();
            window.date = time_parser($('#time').text());
            window.calendar = policy['calendar'];
            setSyncDate();
            display_contextualized_policy(policy['policy'][0]);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

/*
function submit_change_mul(){
    var msgs = [];
    var new_policy = {};
    var msg = {};
    var risk = [];
    var cost = [];
    var ids = [];

    msg.id = $(this).closest($(".qn")).attr('id'); //get the id of a question with changed option

    new_policy.plen=$('input[name="plen"]:checked').val();
    new_policy.psets=$('input[name="psets"]:checked').val();
    if($('input[name="pdict"]:checked').val()==null)
    {
        new_policy.pdict = 0;
    }
    else
    {
        new_policy.pdict = 1;
    }
    if($('input[name="precovery"]:checked').val()==null)
    {
        new_policy.precovery = 0;
    }
    else
    {
        new_policy.precovery = 1;
    }
    //new_policy.pdict=$('input[name="pdict"]:checked').val();
    new_policy.phist=$('input[name="phist"]:checked').val();
    new_policy.prenew=$('input[name="prenew"]:checked').val();
    new_policy.pattempts=$('input[name="pattempts"]:checked').val();
    //new_policy.precovery=$('input[name="precovery"]:checked').val();
    msg.data=JSON.stringify(new_policy);

    msgs.push(msg);

    $(".qn").each(function(i) { //iteration accross questions
        var id_tmp =  $(this).attr('id');

        //msgs = msgs.concat(get_range(new_policy, id_tmp));
    });
//    msgs = msgs.concat(get_range(new_policy, msg.id));
    // console.log(msgs.concat(get_range(new_policy, "plen")));
    var request = $.ajax({
        url: "/score/multiple",
        type: "POST",
        async : false,
        data : JSON.stringify(msgs),
        contentType : "application/json; charset=utf-8",
        dataType : "json",
        success : function(policy_costs_risks) {
            initialize_graphs(policy_costs_risks);
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
        });
    return false;

}
*/



/*
function submit_change() { // old version, which submits all the values even not changed ones
    var d = new Date();
    var msg = {};
    var new_policy = {};
    var day = d.getDate() - 1; // Why is this -1? --Martin
    var strDate = $('#time').text();
    msg.date = strDate;
    msg.userid = document.forms["input"]["userid"].value;
    new_policy.plen = $('input[name="plen"]:checked').val();
    new_policy.psets = $('input[name="psets"]:checked').val();
    new_policy.pdict = $('input[name="pdict"]:checked').val();
    new_policy.phist = $('input[name="phist"]:checked').val();
    new_policy.prenew = $('input[name="prenew"]:checked').val();
    new_policy.pattempts = $('input[name="pattempts"]:checked').val();
    new_policy.precovery = $('input[name="precovery"]:checked').val();
    msg.data = JSON.stringify(new_policy);
    msg.id = window.id_elem;
    msg.recent_cost = calculate_cost_from_calendar();
    msg.prophesize = false;
    console.log(msg);
    //summarize_policy(new_policy); //update policy summary for user

    var request = $.ajax({
        url: "/pwpolicy",
        type: "POST",
        async: false,
        data: JSON.stringify(msg),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (score) {
            console.log("test: " + JSON.stringify(score));
            msg1 = score.msg1;
            msg2 = score.msg2;
            window.calendar = score.calendar;

            visualize(msg2);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
} //old version
*/

send = function() { // need different event handling, to capture any change

    var obj = {};
    var obj1 = {};
    var strDate = document.forms["input"]["date"].value;
    obj.userid=document.forms["input"]["userid"].value;
    obj1.plen=$$('input[name="plen"]:checked').val();
    obj1.psets=$$('input[name="psets"]:checked').val();
    obj1.pdict=$$('input[name="pdict"]:checked').val();
    obj1.phist=$$('input[name="phist"]:checked').val();
    obj1.prenew=$$('input[name="prenew"]:checked').val();
    obj1.pattempts=$$('input[name="pattempts"]:checked').val();
    obj1.precovery=$$('input[name="precovery"]:checked').val();
    obj.data=JSON.stringify(obj1);
    obj.date=strDate;
    console.log(obj);
    var request = jQuery.ajax({
        url: "/forward",
        type: "POST",
        async : false,
        data : JSON.stringify(obj),
        contentType : "application/json; charset=utf-8",
        dataType : "json",
        success : function(score) {
            $$(score).each(function(i) {
                document.forms["input"]["date"].value=score[i].value;
            })
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}


function create_variation(policy, id, value) {
    var new_policy = {};
    for (var key in policy) {
        new_policy[key] = policy[key];
    }
    new_policy[id] = value;

    return new_policy;
}

function get_range(policy, id) {
    var msgs = [];
    $(document).find("#" + id).find('input').each(function (i) {
        var new_policy = create_variation(policy, id, this.value);
        var msg = {};

        msg['id'] = id + this.value;
        msg.data = JSON.stringify(new_policy);
        msgs.push(msg);

    });
    return msgs;
}

function visualize(policy_costs_risks) { //id examples: plen, psets, pdict, etc.
//    console.log(policy_costs_risks);
//    function initialize_graphs(policy_costs_risks) { //id examples: plen, psets, pdict, etc.
        console.log(policy_costs_risks);
        var graph_id = {};
        dps_risk = {};
        dps_cost = {};

        $(".qn").each(function (i) {
            dps_risk[$(this).closest($(".qn")).attr('id')] = [];//initializing dps
            dps_cost[$(this).closest($(".qn")).attr('id')] = [];//initializing dps
            graph_id[$(this).closest($(".qn")).attr('id')] = "graph_" + [$(this).closest($(".qn")).attr('id')]; //assigning graph ids like graph_id.plen = "graph_plen"
        });

        $(policy_costs_risks).each(function (i) {
            if (this.id.replace(/[a-z]+/, '') != '') {//skip ids without value numbers to avoid duplicate data (e.g. plen)
                var new_string = this.id.replace(/[0-9]+/, ''); // removing numbers from plen0 etc.
                tmpRisk = {label: this.id, y: this.risk};
                tmpCost = {label: this.id, y: this.cost};
                dps_risk[new_string].push(tmpRisk);
                dps_cost[new_string].push(tmpCost);
            } else {
                console.log(this);
                $("#risk").text(verboseScore(this.risk));
                $("#cost").text(verboseScore(this.cost));
            }
        });
        console.log("Initializing graphs details(ids, risks, costs)...");
//    console.log(graph_id);
//    console.log(dps_risk);
//    console.log(dps_cost);

        display_graphs(graph_id, dps_risk, dps_cost);
    }

    function display_graphs(graph_id, dps_risk, dps_cost) {

        $(".qn").each(function (i) {

            var chart = new CanvasJS.Chart(graph_id[$(this).closest($(".qn")).attr('id')], { //processing graph for each question
                /*
                title: {
                    text: "Risk and Cost"
                },
                axisX: {
                    title: $(this).closest($(".qn")).attr('id')
                },
                */
                axisY: {
                    title: "Risk / PC"
                },
                // begin data for 2 line graphs. Note dps1 and dps2 are
                //defined above as a json object. See http://www.w3schools.com/json/
                data: [

                    { type: "line", color: "#369ead",name: "PC", /*showInLegend: true,*/ dataPoints: dps_cost[$(this).closest($(".qn")).attr('id')]}, //blue
                    { type: "line", color: "#c24642",/*name: "R", showInLegend: true,*/ dataPoints: dps_risk[$(this).closest($(".qn")).attr('id')]} //red
                ]
                // end of data for 2 line graphs
            }); // End of new chart variable
        chart.render();
        });

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
            console.log(val);
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
        manage_toast_alert('Please, select two distinct options or change the number of mechanisms');
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
    })
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
