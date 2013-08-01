timelineModel = {
    currentDate: ko.observable(new Date(0)),
    nextSync: ko.observable(new Date(0)),
    clock: ko.observable()
};

function checkEvents() {
    var tmp_events_calendar = window.calendar;
    $(tmp_events_calendar).each(function (i) {
        if (new Date(tmp_events_calendar[i].date) - timelineModel.currentDate() === 0) {
            $('#pause').click();
            tmp_event = tmp_events_calendar[i].events
            $(tmp_event).each(function (j) {
                display_event(tmp_event[j].incdt_id, tmp_event[j].cost);
                submit_event($.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate()));
            })
            $('.incident_page').click();
        }
    })
}

function submit_event(date) {
    $.ajax({
        url: "api/chronos/event",
        type: "POST",
        data: JSON.stringify({date: date}),
        success: function (response) {
            console.log("success: " + response.messages[0]);
        },
        error: function (response) {
            console.log("fail: " + response.messages[0]);
        }
    });
}

function submitPolicyDelta() { // need different event handling, to capture any change
    var msg = {
        date: $.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate()),
        policyUpdate: [],
        initPolicy: true
    };
    if (policyUpdate.length > 0) {
        msg.policyUpdate = policyUpdate;
    }
    console.log(msg);
    statusUpdating();
    $.ajax({
        url: "api/chronos/update",
        type: "POST",
        data: JSON.stringify(msg),
        success: update_policy,
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function resume() {
    statusUpdating();
    $.ajax({
        url: "api/chronos/resume",
        type: "GET",
        success: function (policy) {
            policyUpdate = [];
            statusReady();
            $('#pause').click();
            timelineModel.currentDate(new Date(policy['date']))
            window.calendar = policy['calendar'];
            display_contextualized_policy(policy['policy'][0]);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function startClock(interval) {
    console.log("clock started");
    if (timelineModel.clock() != undefined) pauseClock();
    timelineModel.clock(setInterval(function () {

        timelineModel.currentDate().setDate(timelineModel.currentDate().getDate()+1);
        timelineModel.currentDate.valueHasMutated();

    }, interval));
}

function pauseClock() {
    clearInterval(timelineModel.clock());
}

$(function () {

    ko.applyBindings(timelineModel, document.getElementById('timeline'));

    timelineModel.currentDate.subscribe(function () {

        if (timelineModel.currentDate() - timelineModel.nextSync() === 0) {
            toastr['success']("Changes submitted");
            $('#pause').click();
            submitPolicyDelta();
        }

        timelineModel.nextSync(new Date(timelineModel.currentDate().getFullYear(), timelineModel.currentDate().getMonth()+1, 1));

        checkEvents();
        updateCharacters($.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate())); //specified in characters.js

        window.id_elem = 'plen';

        if (timelineModel.currentDate - new Date('2014-2-1') < 0) {
            //console.log('less than 1 month passed. Score is not yet calculated, hide button');
            $(".score_page").hide();
        } else {
            //console.log('>=1 month passed. Score is calculated, show button.');
            $(".score_page").show();
        }
        $(".incident_page").hide();
    })

})

function format_date(date) {
    return $.datepicker.formatDate($.datepicker.RFC_1123, date)
}