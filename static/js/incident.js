function initIncident() {
    sendIncidentRequest();
}


sendIncidentRequest = function() { // need different event handling, to capture any change
 var request = jQuery.ajax({
 url: "/forward",
 type: "GET",
 async : false,
 success : function(incident) {
 $$(incident).each(function(i) {
 console.log(this);
 //document.forms["input"]["date"].value=score[i].value;
 })
 },
 error: function(response) {
 console.log("fail: " + response.responseText);
 }
 });
 return false;
 }