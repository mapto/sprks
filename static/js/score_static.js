/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 05.07.13
 * Time: 14:51
 * To change this template use File | Settings | File Templates.
 */

function initScoreStatic(){
    var request = jQuery.ajax({
        url: "/score_static",
        type: "GET",
        async : false,

        success : function(score) {
            console.log(score);
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;

}
