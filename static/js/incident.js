function get_incident_data(incident_id) {
    statusUpdating();
    $.ajax({
        url: "api/incident/"+incident_id,
        type: "GET",
        success: function (incident) {
            statusReady();
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
}

function display_event(incident_id, cost){
    // Handles trigger for when certain event occurs.
    get_incident_data(incident_id);
    $("#monetary_cost").text(cost);
    $(".incident_page").show();
    toastr['warning']('Incident occurred!')
}