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

            incidentModel.incidentDate(new Date(timelineModel.currentDate()));
            incidentModel.description(incident.description);
            incidentModel.event(incident.event);
            incidentModel.consequences(incident.consequences);
            incidentModel.riskType(incident.type);
            incidentModel.risk(incident.risk);

            charactersModel.quote1(incident.description);
            charactersModel.quote2(incident.description);
            charactersModel.quote3(incident.description);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function displayEvent(incident){
    // Handles trigger for when certain event occurs.
    getIncidentDetails(incident.incdt_id);
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
        success: function (event) {
            if(event.length>2){

                event = JSON.parse(event);

                $.ajax({
                url: "api/incident/"+event.incident_id,
                type: "GET",
                success: function (incident) {
                    statusReady();
                    incidentModel.incidentDate(new Date(event.date));
                    incidentModel.description(incident.description);
                    incidentModel.event(incident.event);
                    incidentModel.consequences(incident.consequences);
                    incidentModel.riskType(incident.type);
                    incidentModel.risk(incident.risk);

                    incidentModel.monetaryCost(event.cost);
                    incidentModel.employee(event.employee);
                    incidentModel.location(event.location);
                    incidentModel.device(event.device);

                    charactersModel.quote1(incident.description);
                    charactersModel.quote2(incident.description);
                    charactersModel.quote3(incident.description);
                },
                error: function (response) {
                    console.log("fail: " + response.responseText);
                }
            });

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