/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/25/13
 * Time: 10:35 AM
 * To change this template use File | Settings | File Templates.
 */
//function for moving characters (class interviewee, ids:interviewee1,interviewee2,interviewee3)

    var coordinates = {};
    coordinates.interviewee1 = {}; //Susie
    coordinates.interviewee2 = {}; //Kevin
    coordinates.interviewee3 = {}; //Iza

    coordinates.interviewee1.home = [40, 55, 55];
    coordinates.interviewee1.public = [55, 40, 20];
    coordinates.interviewee1.office = [15, 80, 20];

    coordinates.interviewee2.home = [47.5, 47.5, 55];
    coordinates.interviewee2.public = [62.5, 32.5, 20];
    coordinates.interviewee2.office = [22.5, 72.5, 20];

    coordinates.interviewee3.home = [55, 40, 55];
    coordinates.interviewee3.public = [70, 25, 20];
    coordinates.interviewee3.office = [30, 65, 20];


    function placeDiv(div_id, l_pos, r_pos, b_pos) {
        var d = document.getElementById(div_id);
        d.style.left = (l_pos)+'%';
        d.style.right = (r_pos)+'%';
        d.style.bottom = (b_pos)+'%';
    }

    function place_at(div_id, place){
        var l = coordinates[div_id][place][0];
        var r = coordinates[div_id][place][1];
        var b = coordinates[div_id][place][2];
        placeDiv(div_id, l,r,b);                                        //update charachter position
        placeDiv('quote'+div_id.substr(div_id.length-1),l-12.5,r+12.5,b+18);  //update position of his speech bubble
    }



    function give_device(div_id, device){
        var device_img = 'static/img/'+device+'.png';
        //formModel[div_id+'_device_image']('static/img/'+device+'.png');
    }



    function UpdateCharacters(date){ //data: interviewee1 - location, device; interviewee2 - loc, dev; interviewee3 - loc, dev

        var request = $.ajax({
            url: "/api/characters",
            type: "GET",
            async: false,
            data: JSON.stringify(date),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                console.log(data);
                $.each(data, function(key,value) {
                    place_at(key, value[0]);       //e.g.: place_at('interviewee2', 'office');
                    give_device(key, value[1]);    //e.g.: give_device('interviewee1, 'phone');
                });
            },
            error: function (response) {
                console.log("fail: " + response.responseText);
            }
        });
        return false;
    }


$(function(){
    formModel.interviewee1_device_image('static/img/laptop.png');
    formModel.interviewee2_device_image('static/img/desktop.png');
    formModel.interviewee3_device_image('static/img/iphone.png');
})