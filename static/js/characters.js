//function for moving characters (class interviewee, ids:interviewee1,interviewee2,interviewee3)

intervieweeDeviceModel = {
    interviewee1_device_image: ko.observable(),
    interviewee2_device_image: ko.observable(),
    interviewee3_device_image: ko.observable()
};

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
    d.style.left = (l_pos) + '%';
    d.style.right = (r_pos) + '%';
    d.style.bottom = (b_pos) + '%';

    if ($('#' + div_id).attr('id').substr(0, 5) === 'quote') {
        var t_pos = 100 - b_pos - 20;
        d.style.top = (t_pos) + '%';
    }
}

function place_at(div_id, place) {
    var l = coordinates[div_id][place][0];
    var r = coordinates[div_id][place][1];
    var b = coordinates[div_id][place][2];
    placeDiv(div_id, l, r, b);                                        //update charachter position
    placeDiv('quote' + div_id.substr(div_id.length - 1), l - 12.5, r + 12.5, b + 18);  //update position of his speech bubble
}

function give_device(div_id, device) {
    intervieweeDeviceModel[div_id + '_device_image']('static/img/' + device + '.png');
}

function UpdateCharacters(date) { //data: interviewee1 - location, device; interviewee2 - loc, dev; interviewee3 - loc, dev
    msg = {};
    msg['date'] = date;
    var request = $.ajax({
        url: "/api/characters",
        type: "POST",
        data: JSON.stringify(msg),
        contentType: "application/json; charset=utf-8",
        dataType: "application/json",
        success: function (data) {
            data_tmp = json.parse(data);
            $.each(data_tmp, function (key, value) {
                place_at(key, value[0]);       //e.g.: place_at('interviewee2', 'office');
                give_device(key, value[1]);    //e.g.: give_device('interviewee1, 'phone');
            });
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

$(function () {

    ko.applyBindings(intervieweeDeviceModel, document.getElementById('map'));

    intervieweeDeviceModel.interviewee1_device_image('static/img/laptop.png');
    intervieweeDeviceModel.interviewee2_device_image('static/img/desktop.png');
    intervieweeDeviceModel.interviewee3_device_image('static/img/phone.png');
});