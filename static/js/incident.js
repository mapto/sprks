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

                    var quotes = [
                    "The main problem I have with my job is that IT support is terrible. It used to be the case that the department was in the same building, and you knew you could walk in or call them up and speak to the same people you spoke to last time. A bottle of wine at Christmas kept them happy and I always got things fixed in time. Now it is some random person half the world away that doesn't know me from Adam. Not having that personal relationship makes things more difficult and everything takes twice as long to get fixed. This can be a real problem when the boss is under pressure and the latest round of password changes has locked me out of his email account.",
                    "I have been re-hired to do the same job, at the same level of pay, but without benefits. It doesn't make me happy but there are no other decent IT jobs going in this area, so I have to do it. Unfortunately they know this too and so we don’t get treated like we did when I worked here properly. It doesn't help that with all the shuffling around no-one knows each other anymore. We all have to wear badges now, use passwords everywhere, walk through checkpoints like we are at the airport every time we want to go to the toilet. That’s what it seems like to me anyway. I walk all over the building fixing computers and stuff and the atmosphere really has changed.",
                    "My job sounds fancier than it is, I don’t really manage anyone, just look after some clients. Have the mergers affected me? I suppose so. It got pretty confusing for a while, who was working on what and who was allowed to see the info I have on our customers. It seemed to take ages to get any changes made to permissions but we have always had a few tricks to deal with that. The merger didn’t make that side of things worse, but for a while you never know who you would be working with from one week to the next. I am glad it has settled down now, I am starting to get friendly with my new team and that makes work go a little easier."
                    ];

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