incidentModel = {
    incidentDate: ko.observable(new Date(0)),
    description: ko.observable(''),
    event: ko.observable(''),
    consequences: ko.observable(''),
    riskType: ko.observable(''),
    risk: ko.observable(0),
    monetaryCost: ko.observable(0)
}

function getIncidentDetails(incident_id) {
    statusUpdating();
    $.ajax({
        url: "api/incident/"+incident_id,
        type: "GET",
        success: function (incident) {
            statusReady();

            incidentModel.incidentDate(new Date(timelineModel.currentDate()));
            incidentModel.description(incident.description);
            incidentModel.event(incident.event);
            incidentModel.consequences(incident.consequences);
            incidentModel.riskType(incident.riskType);
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
    getIncidentDetails(incident_id);
    incidentModel.monetaryCost(cost);
    $(".incident_page").show();
    toastr.warning('Incident occurred!')
}

$(function(){
    ko.applyBindings(incidentModel, document.getElementById('incident_page'))
})