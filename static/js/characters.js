/*function for moving characters (class interviewee, ids:interviewee1,interviewee2,interviewee3)*/
var quotes = [
    "My responsibility is to make sure that offshore operations of the company continue to grow and run efficiently and safely. To access information about this operations I need to login to the system on a regular basis",
    "I have been re-hired to do the same job, at the same level of pay, but without benefits. It doesn't make me happy but there are no other decent IT jobs going in this area, so I have to do it. Unfortunately they know this too and so we don’t get treated like we did when I worked here properly. It doesn't help that with all the shuffling around no-one knows each other anymore. We all have to wear badges now, use passwords everywhere, walk through checkpoints like we are at the airport every time we want to go to the toilet. That’s what it seems like to me anyway. I walk all over the building fixing computers and stuff and the atmosphere really has changed.",
    "My job sounds fancier than it is, I don’t really manage anyone, just look after some clients. Have the mergers affected me? I suppose so. It got pretty confusing for a while, who was working on what and who was allowed to see the info I have on our customers. It seemed to take ages to get any changes made to permissions but we have always had a few tricks to deal with that. The merger didn’t make that side of things worse, but for a while you never know who you would be working with from one week to the next. I am glad it has settled down now, I am starting to get friendly with my new team and that makes work go a little easier.",
    "The main problem I have with my job is that IT support is terrible. It used to be the case that the department was in the same building, and you knew you could walk in or call them up and speak to the same people you spoke to last time. A bottle of wine at Christmas kept them happy and I always got things fixed in time. Now it is some random person half the world away that doesn't know me from Adam. Not having that personal relationship makes things more difficult and everything takes twice as long to get fixed. This can be a real problem when the boss is under pressure and the latest round of password changes has locked me out of his email account.",
    "I promote energy saving products, on a door-to-door basis through calling the potential clients and face to face meetings. I have to login to the system to access their details.",
    "I have to source and select candidates in accordance with their skills, so that they match perfectly with the vacancies within our company. I need to login to the system to access the skills required for a variety of positions.",
    "My responsibility is to coordinate any contract legal disputes or discussions as the main lead for the company in the local and regional market area. I have to login to the system to access the database of contracts.",
    "I have to establish continuous supplier performance improvement plans , develop and maintain an annual supplier quality assurance and inspection. I have to login to the system to retrieve the information about suppliers.",
    "I am responsible for assigning, managing and overseeing all projects within the company. I have to login to the system to access the information about the projects and the employees assigned."
];

charactersModel = {
    currentQuote: ko.observable(0),
    interviewee1DeviceImage: ko.observable('static/img/laptop.png'),
    interviewee2DeviceImage: ko.observable('static/img/desktop.png'),
    interviewee3DeviceImage: ko.observable('static/img/phone.png'),
    interviewee4DeviceImage: ko.observable('static/img/laptop.png'),
    interviewee5DeviceImage: ko.observable('static/img/desktop.png'),
    interviewee6DeviceImage: ko.observable('static/img/phone.png'),
    interviewee7DeviceImage: ko.observable('static/img/laptop.png'),
    interviewee8DeviceImage: ko.observable('static/img/desktop.png'),
    interviewee9DeviceImage: ko.observable('static/img/phone.png'),
    quote1: ko.observable(''),
    quote2: ko.observable(''),
    quote3: ko.observable(''),
    quote4: ko.observable(''),
    quote5: ko.observable(''),
    quote6: ko.observable(''),
    quote7: ko.observable(''),
    quote8: ko.observable(''),
    quote9: ko.observable(''),
    interviewee1Location: ko.observable(''),
    interviewee2Location: ko.observable(''),
    interviewee3Location: ko.observable(''),
    interviewee4Location: ko.observable(''),
    interviewee5Location: ko.observable(''),
    interviewee6Location: ko.observable(''),
    interviewee7Location: ko.observable(''),
    interviewee8Location: ko.observable(''),
    interviewee9Location: ko.observable('')
};

var coordinates = {};
coordinates.interviewee1 = {}; //Andrew
coordinates.interviewee2 = {}; //Kevin
coordinates.interviewee3 = {}; //Iza
coordinates.interviewee4 = {}; //Susie
coordinates.interviewee5 = {}; //Richard
coordinates.interviewee6 = {}; //Helen
coordinates.interviewee7 = {}; //Karine
coordinates.interviewee8 = {}; //Drake
coordinates.interviewee9 = {}; //Hue

coordinates.interviewee1.home = [40, 55, 53];
coordinates.interviewee1.public = [55, 40, 18];
coordinates.interviewee1.office = [15, 80, 18];

coordinates.interviewee2.home = [47.5, 47.5, 53];
coordinates.interviewee2.public = [62.5, 32.5, 18];
coordinates.interviewee2.office = [22.5, 72.5, 18];

coordinates.interviewee3.home = [55, 40, 53];
coordinates.interviewee3.public = [70, 25, 18];
coordinates.interviewee3.office = [30, 65, 18];

coordinates.interviewee4.home = [36, 59, 63];
coordinates.interviewee4.public = [51, 44, 28];
coordinates.interviewee4.office = [11, 84, 28];

coordinates.interviewee5.home = [43.5, 43.5, 63];
coordinates.interviewee5.public = [58.5, 36.5, 28];
coordinates.interviewee5.office = [18.5, 76.5, 28];

coordinates.interviewee6.home = [51, 44, 63];
coordinates.interviewee6.public = [66, 29, 28];
coordinates.interviewee6.office = [26, 69, 28];

coordinates.interviewee7.home = [40, 55, 73];
coordinates.interviewee7.public = [55, 40, 38];
coordinates.interviewee7.office = [15, 80, 38];

coordinates.interviewee8.home = [47.5, 47.5, 73];
coordinates.interviewee8.public = [62.5, 32.5, 38];
coordinates.interviewee8.office = [22.5, 72.5, 38];

coordinates.interviewee9.home = [55, 40, 73];
coordinates.interviewee9.public = [70, 25, 38];
coordinates.interviewee9.office = [30, 65, 38];

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

function placeAt(div_id, place) {
    var l = coordinates[div_id][place][0];
    var r = coordinates[div_id][place][1];
    var b = coordinates[div_id][place][2];
    placeDiv(div_id, l, r, b);                                        //update character position
    placeDiv('quote' + div_id.substr(div_id.length - 1), l - 12.5, r + 12.5, b + 10);  //update position of his speech bubble
}

function giveDevice(div_id, device) {
    charactersModel[div_id + 'DeviceImage']('static/img/' + device + '.png');
}

//flag to avoid characters saying events several times a day:
var events_flag = [];
//flag to avoid characters telling about the same events:
var char_flag = {'executives':0,'desk':0,'road':0};
function updateCharacters(date) { //data: interviewee1 - location, device; interviewee2 - loc, dev; interviewee3 - loc, dev
    $.ajax({
        url: "api/characters",
        type: "POST",
        data: JSON.stringify({date:date}),
        success: function (data) {
            $.each(data, function (key, value) {
                placeAt(key, value[0]);       //e.g.: placeAt('interviewee2', 'office');
                giveDevice(key, value[1]);    //e.g.: giveDevice('interviewee1, 'phone');
                charactersModel[key + 'Location'](value[0]); //e.g. charactersModel.interviewee1Location(office)
                /* //commented out incidents
                var charSet= ['executives','desk','road'];
                for (var k in timelineModel.calendar()){
                    var event = timelineModel.calendar()[k]['events'];
                    for (var ev in event){
                        for (var em in charSet){
                            var i = parseFloat(em)+1;
                            //assign event for each character's quote from the calendar
                            if((event[ev].employee==charSet[em])){
                               if(event[ev].device + '.png'== (charactersModel['interviewee'+i+ 'DeviceImage']()).replace("static/img/","") ){
                                   if(event[ev].location == charactersModel['interviewee'+i+ 'Location']()){
                                       if (char_flag[event[ev].employee]!=1 && jQuery.inArray(k, events_flag)<0 ){
                                       //char_flag is for limiting amount of events per character to 1 for 1 tick of timer, events_flag is to avoid the same events to be quoted several times

                                           char_flag[event[ev].employee]=1;
                                           events_flag.push(k);
                                           $.ajax({
                                            url: "api/incident/"+event[ev].incdt_id,
                                            type: "GET",
                                            async:false, //had to set to async:false, as if it is async, em and i variable keep incrementing while the request is sent
                                            success: function (incidnt) {
                                                charactersModel['quote'+i](incidnt.description); //executive, road or desk
                                                $('#interviewee'+i).click();
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
                    }
                }
                */
            });
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

$("#interviewee1").click(function () {
    if (charactersModel.currentQuote() === 1) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(1);
    }
});
$("#interviewee2").click(function () {
    if (charactersModel.currentQuote() === 2) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(2);
    }
});
$("#interviewee3").click(function () {
    if (charactersModel.currentQuote() === 3) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(3);
    }
});
$("#interviewee4").click(function () {
    if (charactersModel.currentQuote() === 4) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(4);
    }
});
$("#interviewee5").click(function () {
    if (charactersModel.currentQuote() === 5) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(5);
    }
});
$("#interviewee6").click(function () {
    if (charactersModel.currentQuote() === 6) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(6);
    }
});
$("#interviewee7").click(function () {
    if (charactersModel.currentQuote() === 7) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(7);
    }
});
$("#interviewee8").click(function () {
    if (charactersModel.currentQuote() === 8) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(8);
    }
});
$("#interviewee9").click(function () {
    if (charactersModel.currentQuote() === 9) {
        charactersModel.currentQuote(0);
    } else {
        charactersModel.currentQuote(9);
    }
});
$(document).click(function (e) {
    if (e.target.className !== 'interviewee') {
        charactersModel.currentQuote(0);
    }
});

$(function () {
    charactersModel.quote1(quotes[0]);
    charactersModel.quote2(quotes[1]);
    charactersModel.quote3(quotes[2]);
    charactersModel.quote4(quotes[3]);
    charactersModel.quote5(quotes[4]);
    charactersModel.quote6(quotes[5]);
    charactersModel.quote7(quotes[6]);
    charactersModel.quote8(quotes[7]);
    charactersModel.quote9(quotes[8]);
});
