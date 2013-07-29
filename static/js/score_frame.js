/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/29/13
 * Time: 10:27 AM
 * To change this template use File | Settings | File Templates.
 */
function get_score_frame(){
    var risk;
    var cost;
    var request = jQuery.ajax({
        url: "/api/score_frame", //function specified in incident.html
        type: "GET",
        async:false,
        success : function(data) {
            if(data){
                data = JSON.parse(data);
                var score_frame = []
                score_frame.push(data[data.length-1]);
                score_frame.push(data[data.length-2]);
                $(score_frame).each(function(){
                    if(this.score_type==='1'){
                        risk = this.score_value;
                    }else if(this.score_type==='2'){
                        cost = this.score_value;
                    }
                });
                $('#risk_menu').text(verboseScore(risk));
                $('#cost_menu').text(verboseScore(cost));
                if($('#risk_menu').text()||$('#cost_menu').text()){
                    $('.risk-menu').css('display', 'block');
                    //console.log('found data for score_frame');
                }
            }
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}
