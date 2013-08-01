incidentModel = {
    description: ko.observable(),
    event: ko.observable(),
    consequences: ko.observable(),
    risk: ko.observable(),
    monetaryCost: ko.observable()
}

function get_incident_data(incident_id) {
    statusUpdating();
    $.ajax({
        url: "api/incident/"+incident_id,
        type: "GET",
        success: function (incident) {
            statusReady();

            incidentModel.description(incident.description);
            incidentModel.event(incident.event);
            incidentModel.consequences(incident.consequences);
            incidentModel.risk(incident.risk);

            $('#quote1').text(incident.description);
            $('#quote2').text(incident.description);
            $('#quote3').text(incident.description);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function display_event(incident_id, cost){
    // Handles trigger for when certain event occurs.
    get_incident_data(incident_id);
    incidentModel.monetaryCost(cost);
    $(".incident_page").show();
    toastr['warning']('Incident occurred!')
}

$(function(){
    ko.applyBindings(incidentModel, document.getElementById('incident_page'))
})