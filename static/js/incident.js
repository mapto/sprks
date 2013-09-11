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
        success: function (events) {
            if(events.length>2){
                events = JSON.parse(events);
                var event = events[0];

                //TODO assign quotes to characters from a range of events depending on a kind of employee, its location, device
                    //now the latest happened event is assigned to all employees no matter of their type, location or device
                    //assign event for a character1's quote
                    var charSet= ['executives','desk','road'];
                    var flag = {};flag.executives = 0;flag.road = 0;flag.desk = 0; //flag for allowing only a unique initialisation of a quote
                    for (var k in events){
                        console.log(events[k]);
                        for (var j in charSet){
                            var i = parseFloat(j)+1;
                            //assign event for each character's quote
                            if((flag[charSet[j]]<1) && (events[k].employee==charSet[j])){
                               if(events[k].device + '.png'== (charactersModel['interviewee'+i+ 'DeviceImage']()).replace("static/img/","") ){
                                   if(events[k].location == charactersModel['interviewee'+i+ 'Location']()){
                                        $.ajax({
                                        url: "api/incident/"+events[k].incident_id,
                                        type: "GET",
                                        success: function (incidnt) {
                                            incidentModel.description(incidnt.description);
                                            charactersModel['quote'+i](incidnt.description); //executive, road or desk
                                        },
                                        error: function (response) {
                                            console.log("fail: " + response.responseText);
                                        }
                                        });
                                   }
                               }
                            }
                        }
                    }
                //////end of characters handling event

                //request for handling the incident page resuming on login
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

                    //these 3 lines to be removed once the quotes proper assignment (above) is implemented
                    charactersModel.quote1(incident.description); //executive
                    charactersModel.quote2(incident.description); //road
                    charactersModel.quote3(incident.description); //desk
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