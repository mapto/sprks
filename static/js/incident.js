/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 02.07.13
 * Time: 15:19
 * To change this template use File | Settings | File Templates.
 */
function initIncident(){

    var incident;
    var request = jQuery.ajax({
        url: get_filename(),
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

}
