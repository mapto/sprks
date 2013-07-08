/**
 * Created with PyCharm.
 * User: Zhanelya
 * Date: 02.07.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */

var incident;
var incident_name;
function initIncident(){
    window.timer1 = setInterval(function(){alert("Hello")},5000);

    get_incident_name();

    var request = jQuery.ajax({
        url: get_filename(), //function specified in incident.html
        type: "GET",
        success : function(data) {
            incident = JSON.parse(data);
            $(".incident_box").each(function(){
                $(this).text(incident[ ($(this).attr('id')) ]);
            });
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function get_filename(){
        var filename = '/static/incidents/'+incident_name+'.json';
        return filename;
    }

function get_incident_name(){
    var request = jQuery.ajax({
        url: "/incident_rest", //function specified in incident.html
        type: "GET",
        async:false,
        success : function(name) {
            incident_name = name;
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

