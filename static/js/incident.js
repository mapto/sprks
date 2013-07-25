/**
 * Created with PyCharm.
 * User: Zhanelya
 * Date: 02.07.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */

var incident;
function initIncident() {
//    window.timer1 = setInterval(function(){alert("Hello")},5000);

    get_incident_name();
}

function get_filename(incident_name) {
    return '/static/incidents/' + incident_name + '.json';
}

function get_incident_name() {
    statusUpdating();
    $.ajax({
        url: "/incident_rest", //function specified in incident.html
        type: "GET",
        success: get_incident_data,
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function get_incident_data(name) {
    $.ajax({
        url: get_filename(name), //function specified in incident.html
        type: "GET",
        // cache: false,
        success: function (incident) {
            statusReady();
            incident = JSON.parse(incident);
            $(".incident_box").each(function () {
                $(this).text(incident[ ($(this).attr('id')) ]);
            });
            $('#quote1').text(incident['description']);
            $('#quote2').text(incident['description']);
            $('#quote3').text(incident['description']);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}