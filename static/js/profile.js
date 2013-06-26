/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 25.06.13
 * Time: 16:27
 * To change this template use File | Settings | File Templates.
 */
function init() {
 /*Only a reminder what the data is being sent */
 json1=json[0];
 var prenew = ( json1.prenew);
            var pattempts = ( json1.pattempts);
            var cost = ( json1.cost);
            var idpolicy = ( json1.idpolicy);
            var psets = ( json1.psets);
            var phist = ( json1.phist);
            var userid = ( json1.userid);
            var pautorecover = ( json1.pautorecover);
            var date = ( json1.date);
            var plen = ( json1.plen);
            var risk = ( json1.risk);
            var pdict = ( json1.pdict);
 /*****/

 createGraph(date,cost,risk,json);

 //create table dynamically:
            var table = $('<table></table>').addClass('profile_table');
            //provide column names:
            var row = $('<tr></tr>').addClass('profileTr');
                var date = $('<td></td>').addClass('profileTd_date profileTh_date').text("date");
                    row.append(date);
            for(var j in json[0]){

                var attrName = j; //e.g. pdict
                var col = $('<td></td>').addClass('profileTd').text(attrName);
                if(attrName!=='date'&&attrName!=='idpolicy'&&attrName!=='userid'&&attrName!=='cost'&&attrName!=='risk'){ //do not show these fields
                             row.append(col);
                }
            }
            table.append(row);

            //fill table:
            for(var i in json){
                var obj = json[i]
                var row = $('<tr></tr>').addClass('profileTr');
                    var date = $('<td></td>').addClass('profileTd_date').text(obj['date']);
                    row.append(date);
                    for(var k in obj){

                         var attrName = k; //e.g. pdict
                         var attrValue = obj[k]; //e.g. 1
                         var col = $('<td></td>').addClass('profileTd').text(attrValue);

                         if(attrName!=='date'&&attrName!=='idpolicy'&&attrName!=='userid'&&attrName!=='cost'&&attrName!=='risk'){ //do not show these fields
                             row.append(col);
                         }
                    }
                table.append(row);
            }

            $('#profile_table').append(table);
}


function createGraph(date,cost,risk, data){
    dps1_1 = [];
    dps2_1 = [];
    for(var k in data)
    {
        tmpRisk = {label:data[k].date, y:data[k].risk};
        tmpCost = {label:data[k].date, y:data[k].cost};
        dps1_1.push(tmpRisk);
        dps2_1.push(tmpCost);
    }

    var dps1 = [ {label: date, y: risk},{label: date, y: risk + 0.1} ,  {label: date, y: risk-0.2},  {label: date, y: risk},  {label: date, y: risk} ]; //dataPoints – line 1
    var dps2 = [ {label: date, y: cost},{label: date, y: cost + 0.4} ,  {label: date, y: cost+0.1},  {label: date, y: cost+0.6},  {label: date, y: cost} ]; //dataPoints. – line 2
 var chart = new CanvasJS.Chart("chartContainer",{
 title :{
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
 { type: "line", name: "Risk(%) ", showInLegend: true, dataPoints : dps1_1},
 { type: "line", name: "Productivity cost($ million) ", showInLegend: true, dataPoints : dps2_1}
 ]
 // end of data for 2 line graphs

 }); // End of new chart variable

 chart.render();

}
