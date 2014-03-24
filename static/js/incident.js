incidentModel = {
    incidentDate: ko.observable(),
    description: ko.observable(''),
    event: ko.observable(''),
    consequences: ko.observable(''),
    riskType: ko.observable(''),
    risk: ko.observable(0),
    monetaryCost: ko.observable(0),
    employee: ko.observable(''),
    location: ko.observable(''),
    device: ko.observable('')
}

function getIncidentDetails(incident_id) {
    statusUpdating();
    $.ajax({
        url: "api/incident/"+incident_id,
        type: "GET",
        success: function (incident) {
            statusReady();
            incidentModel.description(incident.description);
            incidentModel.event(incident.event);
            incidentModel.consequences(incident.consequences);
            incidentModel.riskType(incident.type);
            incidentModel.risk(incident.risk);

            //should be handled by characters script depending on combination of employee type, location and device
            //commented out incidents
            //charactersModel.quote1(incident.description);
            //charactersModel.quote2(incident.description);
            //charactersModel.quote3(incident.description);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function displayEvent(incident){
    // Handles trigger for when certain event occurs.
    // console.log("incident arrived: ");
    // console.log(incident);
    getIncidentDetails(incident.incdt_id);
    // console.log("incident expanded: ");
    // console.log(incident);
    incidentModel.incidentDate(new Date(timelineModel.currentDate()));
    incidentModel.monetaryCost(incident.cost);
    incidentModel.employee(incident.employee);
    incidentModel.location(incident.location);
    incidentModel.device(incident.device);
    $(".incident_page").show();
    toastr.warning('Incident occurred!')
}

function get_recent_events(){
    console.log('Checking for recent events...');
    statusUpdating();
    $.ajax({
        url: "api/recent_events",
        type: "GET",
        success: function (events) {
            if(events.length>2){
                events = JSON.parse(events);
                var event = events[0];
                incidentModel.incidentDate(new Date(event.date));
                incidentModel.monetaryCost(event.cost);
                incidentModel.employee(event.employee);
                incidentModel.location(event.location);
                incidentModel.device(event.device);
                getIncidentDetails(event.incident_id);

            }else{
                statusReady();
                incidentModel.incidentDate('');
                incidentModel.description('');
                incidentModel.event('');
                incidentModel.consequences('');
                incidentModel.riskType('');
                incidentModel.risk('');
                incidentModel.monetaryCost('');
                incidentModel.employee('');
                incidentModel.location('');
                incidentModel.device('');

                charactersModel.quote1(quotes[0]);
                charactersModel.quote2(quotes[1]);
                charactersModel.quote3(quotes[2]);
            }
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}