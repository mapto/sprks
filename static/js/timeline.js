timelineModel = {
    currentDate: ko.observable(new Date(0)),
    nextSync: ko.observable(new Date(0)),
    clock: ko.observable(),
    clockSpeed: ko.observable(0),
    calendar: ko.observable()
};

function checkEvents() {
    var tmp_events_calendar = timelineModel.calendar();
    $(tmp_events_calendar).each(function (i) {
        if (new Date(tmp_events_calendar[i].date) - timelineModel.currentDate() === 0) {
            timelineModel.clockSpeed(0);
            tmp_event = tmp_events_calendar[i].events;
            $(tmp_event).each(function (j) {
                displayEvent(tmp_event[j]);
                submitEvent($.datepicker.formatDate($.datepicker.ISO_8601, timelineModel.currentDate()));
            });
            $('.incident_page').click();
        }
    })
}

function submitEvent(date) {
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
        success: updatePolicy,
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
            statusReady();
            timelineModel.clockSpeed(0);
            timelineModel.currentDate(new Date(policy['date']));
            timelineModel.calendar(policy['calendar']);
            displayContextualizedPolicy(policy['policy'][0]);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}

function startClock(interval) {
    console.log("Clock started");
    timelineModel.clock(setInterval(function () {
        timelineModel.currentDate().setDate(timelineModel.currentDate().getDate()+1);
        timelineModel.currentDate.valueHasMutated();
    }, interval));
}


$(function () {

    timelineModel.clockSpeed.subscribe(function(clockSpeed){
        switch (clockSpeed){
            case 0:
                $('.target').removeAttr('disabled');
                $('#apply').removeAttr('disabled');
                clearInterval(timelineModel.clock());
                break;
            case 1:
                $('.target').attr('disabled', 'disabled');
                $('#apply').attr('disabled', 'disabled');
                startClock(3000);
                break;
            case 2:
                $('.target').attr('disabled', 'disabled');
                $('#apply').attr('disabled', 'disabled');
                startClock(500);
                break;
        }
    });

    timelineModel.currentDate.subscribe(function (currentDate) {

        if (currentDate - timelineModel.nextSync() === 0) {
            toastr['success']("Changes submitted");
            timelineModel.clockSpeed(0);
            submitPolicyDelta();
        }

        timelineModel.nextSync(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));

        checkEvents();
        updateCharacters($.datepicker.formatDate($.datepicker.ISO_8601, currentDate)); //specified in characters.js

        window.id_elem = 'plen';
    });

});

function format_date(date) {
    return $.datepicker.formatDate($.datepicker.RFC_1123, date)
}