var json;
var policy_history;
var graph_data;
function initProfile() {

    get_profile();

}

function get_profile() {
    //history values in json format from serverside (policy_history.py) by ajax call written to policy_history var
    var request = $.ajax({
        url: "/history_rest",
        type: "GET",
        success: function (data) {
            json = JSON.parse(data);
            policy_history = JSON.parse(json['policy_history']);
            graph_data = JSON.parse(json['graph_data']);

            createGraph(graph_data);

            //create table dynamically:
            var table = $('<table></table>').addClass('profile_table');

            //provide column names:
            var row = $('<tr></tr>').addClass('profileTr');
            var date = $('<td></td>').addClass('profileTd_date profileTh').text("date");
            row.append(date);
            row.append($('<td></td>').addClass('profileTd profileTh').text("employee"));
            row.append($('<td></td>').addClass('profileTd profileTh').text("device"));
            row.append($('<td></td>').addClass('profileTd profileTh').text("location"));
            for (var j in policy_history[0]) {
                var attrName = j; //e.g. pdict
                if (attrName !== 'date' && attrName !== 'id_policy'  && attrName !== 'id'  && attrName !== 'pw_id'  && attrName !== 'bio_id' && attrName !== 'pass_id' && attrName !== 'user_id' && attrName !== 'cost' && attrName !== 'risk' && attrName !== 'location' && attrName !== 'device' && attrName !== 'employee') { //do not show these fields
                    var col = $('<td></td>').addClass('profileTd profileTh').text(attrName);
                    row.append(col);
                }
            }
            table.append(row);
            //fill table:
            var prev_obj = '';
            var row = [];
            var date = [];
            var col = [];
            var location_r = [];
            var device_r = [];
            var employee_r = [];
            var tmp;
            for (var i in policy_history) {
                var obj = policy_history[i];
                col[i] = {};
                row [i] = $('<tr></tr>').addClass('profileTr' + i);
                date [i] = $('<td></td>').addClass('profileTd_date').text(format_date(new Date(obj['date'])));
                row [i].append(date[i]);
                location_r[i] = $('<td></td>').addClass('profileTd location'+i).text(obj['location']);
                device_r[i] = $('<td></td>').addClass('profileTd device'+i).text(obj['device']);
                employee_r[i] = $('<td></td>').addClass('profileTd employee'+i).text(obj['employee']);
                row[i].append(employee_r[i]);
                row[i].append(device_r[i]);
                row[i].append(location_r[i]);
                for (var k in obj) {
                    var attrName = k; //e.g. pdict
                    var attrValue = obj[k]; //e.g. 1

                    if (attrName !== 'date' && attrName !== 'id_policy' && attrName !== 'id'  && attrName !== 'pw_id'  && attrName !== 'bio_id' && attrName !== 'pass_id' && attrName !== 'user_id' && attrName !== 'cost' && attrName !== 'risk' && attrName !== 'location' && attrName !== 'device' && attrName !== 'employee') { //do not show these fields
                        if (i < 1) { //if it's first row
                            col[i][attrName] = $('<td></td>').addClass('profileTd ' + attrName + i).text(attrValue);
                            //row [i].append(col[i][attrName]);//add all policy values
                        } //else if (i > 0 && (obj[k] !== prev_obj[k])) { //if it's second row
                        else {
                            //if (attrName !== 'employee' && attrName !== 'location' && attrName !== 'device' ){
                            //    col[i][attrName] = $('<td></td>').addClass('profileTd '+attrName+i).text('changed from ' + prev_obj[k] + ' to ' + obj[k]);
                            //}else{
                            col[i][attrName] = $('<td></td>').addClass('profileTd ' + attrName + i).text(obj[k]);
                            //}
                            //row [i].append(col[i][attrName]); //add value column only if value have changed
                        } //else {
                        // col[i][attrName] = $('<td></td>').addClass('profileTd '+attrName+i).text('');
                        row [i].append(col[i][attrName]); //add empty column if no changes
                        //}
                    }
                }
                if (row[i].text() != '') { //check if the row contains anything
                    if (row[i].text().substring(10).match(/\d+/g)) { //exclude date, check if the rest row contains number values( such as for plen, etc.)
                        var empty_row = $('<tr></tr>').addClass('profileTr profileTh');
                        for (var x = 0; x < 13; x++) {
                            empty_row.append($('<td></td>').addClass('profileTd profileTh').text(''));
                        }
                        table.append(empty_row);
                    } else {                                      //if row contains only environmental variables (location/employee/device
                        row[i]
                    }
                    table.append(row[i]);
                }
                prev_obj = policy_history[i];
            }
            $('#profile_table').append(table);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

function createGraph(data) {
    var dps_risk = []; //data points for risk
    var dps_cost = []; //data points cost
    for (var k in data) {

        tmpValue = {label: format_date(new Date(data[k].date)), y: parseFloat(data[k].score_value)};
        if (data[k].score_type === '1') {
            dps_risk.push(tmpValue);
        }
        if (data[k].score_type === '2') {
            dps_cost.push(tmpValue);
        }
    }

    var chart = new CanvasJS.Chart("chartContainer", {
        title: {
            text: "Progress"
        },
        axisX: {
            title: "Date"
        },
        axisY: {
            title: "Units"
        },

        data: [
            { type: "line", color: "#499249", name: "Productivity cost($ million) ", showInLegend: true,
                dataPoints: dps_cost
            }, //blue
            { type: "line", color: "#c24642", name: "Risk(%) ", showInLegend: true,
                dataPoints: dps_risk
            } //red  [{label:'bla', y:5}]
        ]
        // end of data for 2 line graphs

    }); // End of new chart variable

    chart.render();

}
