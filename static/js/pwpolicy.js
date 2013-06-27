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
/*
    switch (start_policy.plen) {
        case $("#len0").val():
    		console.log("found plen 0");
	    	$("#len0").prop('checked', true);
            break;
        case $("#len6").val():
		    console.log("found plen 6");
		    $("#len6").prop('checked', true);
	}else if ($:plen==jQuery("#len8").val()){
		console.log("found plen 8");
		jQuery("#len8").prop('checked', true);
	}else if ($:plen==jQuery("#len10").val()){
		console.log("found plen 10");
		jQuery("#len10").prop('checked', true);
	}else if ($:plen==jQuery("#len12").val()){
		console.log("found plen 12");
		jQuery("#len12").prop('checked', true);
	}
*/


	/*preset pswd sets value*/
    console.log("found sets " + start_policy["psets"]);
    $("#sets" + start_policy["psets"]).prop('checked', true);
/*
	if ($:psets==jQuery("#sets1").val()){
		console.log("found sets any");
		jQuery("#sets1").prop('checked', true);
	}else if ($:psets==jQuery("#sets2").val()){
		console.log("found sets 2");
		jQuery("#sets2").prop('checked', true);
	}else if ($:psets==jQuery("#sets3").val()){
		console.log("found sets 3");
		jQuery("#sets3").prop('checked', true);
	}else if ($:psets==jQuery("#sets4").val()){
		console.log("found sets 4");
		jQuery("#sets4").prop('checked', true);
	}else console.log('FOUND error psets=0')
*/
	/*preset pswd dictionary value*/
    console.log("found " + (start_policy["pdict"]?"use":"no") + " dict");
    $("#dic").prop('checked', start_policy["pdict"] == 1);
/*
	if ($:pdict==jQuery("#dic").val()){
		console.log("found use dict");
		jQuery("#dic").prop('checked', true);
	}else{
		console.log('pdict:no')
	}
*/

	/*preset pswd history check
	none: 0
	simple: 1
	strict: 2
	extreme: 3
	*/
    console.log("found phist difficulty " + start_policy["phist"]);
    $("#hist" + start_policy["phist"]).prop('checked', true);
/*
	if ($:phist==jQuery("#hist1").val()){
		console.log("found phist none");
		jQuery("#hist1").prop('checked', true);
	}else if ($:phist==jQuery("#hist2").val()){
		console.log("found phist simple");
		jQuery("#hist2").prop('checked', true);
	}else if ($:phist==jQuery("#hist3").val()){
		console.log("found phist strict");
		jQuery("#hist3").prop('checked', true);
	}else if ($:phist==jQuery("#hist4").val()){
		console.log("found phist extreme");
		jQuery("#hist4").prop('checked', true);
	}
*/


	/*preset pswd renewal period check
	never: 0
	annual: 1
	quarterly: 2
	monthly: 3
	*/
    console.log("found renew " + start_policy["prenew"]);
    $("#renew" + start_policy["prenew"]).prop('checked', true);
/*
	if ($:prenew==jQuery("#renew1").val()){
		console.log("found renew never");
		jQuery("#renew1").prop('checked', true);
	}else if ($:prenew==jQuery("#renew2").val()){
		console.log("found renew annually");
		jQuery("#renew2").prop('checked', true);
	}else if ($:prenew==jQuery("#renew3").val()){
		console.log("found renew quarterly");
		jQuery("#renew3").prop('checked', true);
	}else if ($:prenew==jQuery("#renew4").val()){
		console.log("found renew monthly");
		jQuery("#renew4").prop('checked', true);
	}
*/
	/*preset pswd attempts number check (yes/no)*/
    /* 0 - unlimited, 1 - limit of 10 attempts, 2 - limit of 3 attempts */
    console.log("found attempts " + start_policy["prenew"]);
    $("#renew" + start_policy["pattempts"]).prop('checked', true);

	/*preset pswd recovery option*/
    console.log("found pautorecover " + start_policy["pautorecover"]);
    $("#autorecover").prop('checked', start_policy["pautorecover"] == 1);
/*
	if ($:pautorecover==jQuery("#autorecover").val()){
		console.log("found pautorecover");
		jQuery("#autorecover").prop('checked', true);
	}else{
		console.log('pautorecover:no')
	}
*/

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
