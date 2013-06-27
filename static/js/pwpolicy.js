/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 22/06/13
 * Time: 13:25
 * To change this template use File | Settings | File Templates.
 */
/*wait until document is loaded*/
function init(){
    //submit_change();
    $('.target').change(submit_change);
    $('.target').change(submit_change_mul);

    //$('#play').click(send) // the play message is not sent from here, but from render decoration (views/index-private.html)

	var d = new Date();
	var strDate = d.getDate() + "/" + (d.getMonth()+1) + "/" + d.getFullYear()+", "+ d.getHours()+":"+d.getMinutes();

	//document.getElementById('curr_date').innerHTML = strDate;

	if(!policyExists()){
        // If code executed, then we have a new user
        // Greet them accordingly
		alert('This is your first visit. You can see the policy as it has been left by your predecessor.')
	}

    // contains elements in the following order:
    start_policy = getInitPolicy();

    console.log("found plen " + start_policy["plen"]);
    $("#len" + start_policy["plen"]).prop('checked', true);

	/*preset pswd sets value*/
    console.log("found sets " + start_policy["psets"]);
    $("#sets" + start_policy["psets"]).prop('checked', true);

	/*preset pswd dictionary value*/
    console.log("found " + (start_policy["pdict"]?"use":"no") + " dict");
    $("#dic").prop('checked', start_policy["pdict"] == 1);

    console.log("found phist difficulty " + start_policy["phist"]);
    $("#hist" + start_policy["phist"]).prop('checked', true);

    console.log("found renew " + start_policy["prenew"]);
    $("#renew" + start_policy["prenew"]).prop('checked', true);

	/*preset pswd attempts number check (yes/no)*/
    /* 0 - unlimited, 1 - limit of 10 attempts, 2 - limit of 3 attempts */
    console.log("found attempts " + start_policy["prenew"]);
    $("#renew" + start_policy["pattempts"]).prop('checked', true);

	/*preset pswd recovery option*/
    console.log("found pautorecover " + start_policy["pautorecover"]);
    $("#autorecover").prop('checked', start_policy["pautorecover"] == 1);

    console.log("Policy initialized...");
}

function verboseScore(score) {
    if(score < 0.2)
    {
        return "very low";
    }
    if(score < 0.4)
    {
        return "low";
    }
    if(score < 0.6)
    {
        return "average";
    }
    if(score < 0.8)
    {
        return "high";
    }
    if(score <= 1)
    {
        return "very high";
    }
}

/* handle AJAX (realtime) submission */
/*
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
    obj1.pautorecover=$$('input[name="pautorecover"]:checked').val();
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
//sends data when users press play button
*/
function submit_change() { // need different event handling, to capture any change
    var d = new Date();
    var msg = {};
    var new_policy = {};
    var day = d.getDate()-1; // Why is this -1? --Martin
	var strDate =document.forms["input"]["date"].value;
    msg.date=strDate;
    msg.userid=document.forms["input"]["userid"].value;
    new_policy.plen=$('input[name="plen"]:checked').val();
    new_policy.psets=$('input[name="psets"]:checked').val();
    new_policy.pdict=$('input[name="pdict"]:checked').val();
    new_policy.phist=$('input[name="phist"]:checked').val();
    new_policy.prenew=$('input[name="prenew"]:checked').val();
    new_policy.pattempts=$('input[name="pattempts"]:checked').val();
    new_policy.pautorecover=$('input[name="pautorecover"]:checked').val();
    msg.data=JSON.stringify(new_policy);
    console.log(msg);
    var request = $.ajax({
        url: "/pwpolicy",
        type: "POST",
        async : false,
        data : JSON.stringify(msg),
        contentType : "application/json; charset=utf-8",
        dataType : "json",
        success : function(score) {
            console.log("test: " + JSON.stringify(score));
            $(score).each(function(i) {
                $("#" + score[i].name).text(verboseScore(score[i].value));
            })

        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
        });
    return false;
}

function submit_change_mul(){
    var msgs = [];
    var new_policy = {};
    var msg ={};

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
    if($('input[name="pautorecover"]:checked').val()==null)
    {
        new_policy.pautorecover = 0;
    }
    else
    {
        new_policy.pautorecover = 1;
    }
    //new_policy.pdict=$('input[name="pdict"]:checked').val();
    new_policy.phist=$('input[name="phist"]:checked').val();
    new_policy.prenew=$('input[name="prenew"]:checked').val();
    new_policy.pattempts=$('input[name="pattempts"]:checked').val();
    //new_policy.pautorecover=$('input[name="pautorecover"]:checked').val();
    msg.data=JSON.stringify(new_policy);
    console.log(msgs);
    msgs.push(msg);
    var request = $.ajax({
        url: "/score/multiple",
        type: "POST",
        async : false,
        data : JSON.stringify(msgs),
        contentType : "application/json; charset=utf-8",
        dataType : "json",
        success : function(policy_costs_risks) {
            console.log("success: " + JSON.stringify(policy_costs_risks));
            $(policy_costs_risks).each(function(i) { //iteration accross policies
                //iteration accross policy values

                var cost = policy_costs_risks[i].cost;
                var risk = policy_costs_risks[i].risk;
                var id = policy_costs_risks[i].id;

                display_graph(id, risk,cost);

            })
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
        });
    return false;

}

function display_graph(id, risk, cost){ //id examples: plen, psets, pdict, etc.

    var graphid = "graph_"+id;//find corresponding graph placeholder id

    var dps1 = [];
    var dps2 = [];

    $(document).find("#"+id).find('input').each(function(i) { //find options for corresponding question
        if(this.checked== true){
            tmpRisk = {label:this.value, y:risk};
            tmpCost = {label:this.value, y:cost};
        }else{
            tmpRisk = {label:this.value};
            tmpCost = {label:this.value};
        }
        dps1.push(tmpRisk);
        dps2.push(tmpCost);

    })

    //display graph
    var chart = new CanvasJS.Chart(graphid,{
 title :{
 text: "Risc/cost"
 },
 axisX: {
 title: id
 },
 axisY: {
 title: "result"
 },
 // begin data for 2 line graphs. Note dps1 and dps2 are
 //defined above as a json object. See http://www.w3schools.com/json/
 data: [
 { type: "line", name: "R", showInLegend: true, dataPoints : dps1},
 { type: "line", name: "PC", showInLegend: true, dataPoints : dps2}
 ]
 // end of data for 2 line graphs

 }); // End of new chart variable

 chart.render();







}
