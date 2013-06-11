/*wait until document is loaded*/
jQuery(document).ready(function(){
	var d = new Date();
	var strDate = d.getFullYear() + "/" + (d.getMonth()+1) + "/" + d.getDate();
	document.getElementById(curr_date).innerHTML = strDate;
	if($:notfound==1){
		alert('ID not found, fields are reset to default')
	}
	/*ID is preset inside HTML code*/
		console.log("found id $:id");

	/*preset password (pswd) length value*/
	if ($:plen==jQuery("#len0").val()){
		console.log("found plen 0");
		jQuery("#len0").prop('checked', true);
	}else if ($:plen==jQuery("#len6").val()){
		console.log("found plen 6");
		jQuery("#len6").prop('checked', true);
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

	/*preset pswd sets value*/
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

	/*preset pswd dictionary value*/
	if ($:pdict==jQuery("#dic").val()){
		console.log("found use dict");
		jQuery("#dic").prop('checked', true);
	}else{
		console.log('pdict:no')
	}

	/*preset pswd history check
	none: 0
	simple: 1
	strict: 2
	extreme: 3
	*/
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

	/*preset pswd renewal period check
	never: 0
	annual: 1
	quarterly: 2
	monthly: 3
	*/
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

	/*preset pswd attempts number check (yes/no)*/
	if ($:pattempts==jQuery("#attempts").val()){
		console.log("found use count pswd attempts");
		jQuery("#attempts").prop('checked', true);
	}

	/*preset pswd recovery option*/
	if ($:pautorecover==jQuery("#autorecover").val()){
		console.log("found pautorecover");
		jQuery("#autorecover").prop('checked', true);
	}else{
		console.log('pautorecover:no')
	}
});