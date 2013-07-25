/**
 * Created with PyCharm.
 * User: Zhanelya
 * Date: 02.07.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */

var incident;
function initIncident(){
//    window.timer1 = setInterval(function(){alert("Hello")},5000);

    get_incident_name();
}

function get_filename(incident_name){
        var filename = '/static/incidents/'+incident_name+'.json';
        return filename;
    }

function get_incident_name(){
    var request = jQuery.ajax({
        url: "/incident_rest", //function specified in incident.html
        type: "GET",
        async:false,
        success : get_incident_data,
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function get_incident_data(name) {
    var request = jQuery.ajax({
        url: get_filename(name), //function specified in incident.html
        type: "GET",
        success : function(incident_post) {
            incident = JSON.parse(incident_post);
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