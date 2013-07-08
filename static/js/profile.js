/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 25.06.13
 * Time: 16:27
 * To change this template use File | Settings | File Templates.
 */
var json;
function initProfile() {

    get_profile(); //history values in json format from serverside (policy_history.py) by ajax call written to json var
    console.log(json);
    createGraph(date, cost, risk, json);

    //create table dynamically:
    var table = $('<table></table>').addClass('profile_table');

    //provide column names:
    var row = $('<tr></tr>').addClass('profileTr');
    var date = $('<td></td>').addClass('profileTd_date profileTh').text("date");
    row.append(date);
    for (var j in json[0]) {
        var attrName = j; //e.g. pdict
        if (attrName !== 'date' && attrName !== 'idpolicy' && attrName !== 'userid' && attrName !== 'cost' && attrName !== 'risk') { //do not show these fields
            var col = $('<td></td>').addClass('profileTd profileTh').text(attrName);
            row.append(col);
        }
    }
    table.append(row);

    //fill table:
    var prev_obj = '';
    for (var i in json) {
        var obj = json[i];
        var row = $('<tr></tr>').addClass('profileTr');
        var date = $('<td></td>').addClass('profileTd_date').text(obj['date']);
        row.append(date);
        for (var k in obj) {
            var attrName = k; //e.g. pdict
            var attrValue = obj[k]; //e.g. 1
            if (attrName !== 'date' && attrName !== 'idpolicy' && attrName !== 'userid' && attrName !== 'cost' && attrName !== 'risk') { //do not show these fields
                if (i < 1) { //if it's first row
                    var col = $('<td></td>').addClass('profileTd').text(attrValue);
                    row.append(col);//add all policy values
                } else if (i > 0 && (obj[k] !== prev_obj[k])) { //if it's second row
                    var col = $('<td></td>').addClass('profileTd').text('changed from ' + prev_obj[k] + ' to ' + obj[k]);
                    row.append(col); //add value column only if value have changed
                } else {
                    var col = $('<td></td>').addClass('profileTd').text('');
                    row.append(col); //add empty column if no changes
                }
            }
        }
        table.append(row);
        prev_obj = json[i];
    }

    $('#profile_table').append(table);
}



function get_profile(){
    var request = jQuery.ajax({
        url: "/history_rest", //function specified in incident.html
        type: "GET",
        async:false,
        success : function(data) {
            json = JSON.parse(data);
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}



function createGraph(date, cost, risk, data) {
    dps1_1 = [];
    dps2_1 = [];
    for (var k in data) {
        tmpRisk = {label: data[k].date, y: data[k].risk};
        tmpCost = {label: data[k].date, y: data[k].cost};
        dps1_1.push(tmpRisk);
        dps2_1.push(tmpCost);
    }

    var dps1 = [
        {label: date, y: risk},
        {label: date, y: risk + 0.1} ,
        {label: date, y: risk - 0.2},
        {label: date, y: risk},
        {label: date, y: risk}
    ]; //dataPoints – line 1
    var dps2 = [
        {label: date, y: cost},
        {label: date, y: cost + 0.4} ,
        {label: date, y: cost + 0.1},
        {label: date, y: cost + 0.6},
        {label: date, y: cost}
    ]; //dataPoints. – line 2
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

        // begin data for 2 line graphs. Note dps1 and dps2 are
        //defined above as a json object. See http://www.w3schools.com/json/
        data: [

            { type: "line", color: "#369ead", name: "Productivity cost($ million) ", showInLegend: true, dataPoints: dps2_1}, //blue
            { type: "line", color: "#c24642", name: "Risk(%) ", showInLegend: true, dataPoints: dps1_1} //red
        ]
        // end of data for 2 line graphs

    }); // End of new chart variable

    chart.render();

}
