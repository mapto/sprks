/*function for moving characters (class interviewee, ids:interviewee1,interviewee2,interviewee3)*/
var quotes = [
    "The main problem I have with my job is that IT support is terrible. It used to be the case that the department was in the same building, and you knew you could walk in or call them up and speak to the same people you spoke to last time. A bottle of wine at Christmas kept them happy and I always got things fixed in time. Now it is some random person half the world away that doesn't know me from Adam. Not having that personal relationship makes things more difficult and everything takes twice as long to get fixed. This can be a real problem when the boss is under pressure and the latest round of password changes has locked me out of his email account.",
    "I have been re-hired to do the same job, at the same level of pay, but without benefits. It doesn't make me happy but there are no other decent IT jobs going in this area, so I have to do it. Unfortunately they know this too and so we don’t get treated like we did when I worked here properly. It doesn't help that with all the shuffling around no-one knows each other anymore. We all have to wear badges now, use passwords everywhere, walk through checkpoints like we are at the airport every time we want to go to the toilet. That’s what it seems like to me anyway. I walk all over the building fixing computers and stuff and the atmosphere really has changed.",
    "My job sounds fancier than it is, I don’t really manage anyone, just look after some clients. Have the mergers affected me? I suppose so. It got pretty confusing for a while, who was working on what and who was allowed to see the info I have on our customers. It seemed to take ages to get any changes made to permissions but we have always had a few tricks to deal with that. The merger didn’t make that side of things worse, but for a while you never know who you would be working with from one week to the next. I am glad it has settled down now, I am starting to get friendly with my new team and that makes work go a little easier."
];

charactersModel = {
    currentQuote: ko.observable(0),
    interviewee1DeviceImage: ko.observable('static/img/laptop.png'),
    interviewee2DeviceImage: ko.observable('static/img/desktop.png'),
    interviewee3DeviceImage: ko.observable('static/img/phone.png'),
    quote1: ko.observable(''),
    quote2: ko.observable(''),
    quote3: ko.observable('')
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

function placeAt(div_id, place) {
    var l = coordinates[div_id][place][0];
    var r = coordinates[div_id][place][1];
    var b = coordinates[div_id][place][2];
    placeDiv(div_id, l, r, b);                                        //update character position
    placeDiv('quote' + div_id.substr(div_id.length - 1), l - 12.5, r + 12.5, b + 18);  //update position of his speech bubble
}

function giveDevice(div_id, device) {
    charactersModel[div_id + 'DeviceImage']('static/img/' + device + '.png');
}

function updateCharacters(date) { //data: interviewee1 - location, device; interviewee2 - loc, dev; interviewee3 - loc, dev
    $.ajax({
        url: "api/characters",
        type: "POST",
        data: JSON.stringify({date:date}),
        success: function (data) {
            $.each(data, function (key, value) {
                placeAt(key, value[0]);       //e.g.: placeAt('interviewee2', 'office');
                giveDevice(key, value[1]);    //e.g.: giveDevice('interviewee1, 'phone');
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

$(document).click(function (e) {
    if (e.target.className !== 'interviewee') {
        charactersModel.currentQuote(0);
    }
});

$(function () {
    charactersModel.quote1(quotes[0]);
    charactersModel.quote2(quotes[1]);
    charactersModel.quote3(quotes[2]);
});