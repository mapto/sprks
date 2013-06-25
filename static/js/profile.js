/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 25.06.13
 * Time: 16:27
 * To change this template use File | Settings | File Templates.
 */
function init() {
 json=json[0];
 var prenew = ( json.prenew);
            var pattempts = ( json.pattempts);
            var cost = ( json.cost);
            var idpolicy = ( json.idpolicy);
            var psets = ( json.psets);
            var phist = ( json.phist);
            var userid = ( json.userid);
            var pautorecover = ( json.pautorecover);
            var date = ( json.date);
            var plen = ( json.plen);
            var risk = ( json.risk);
            var pdict = ( json.pdict);
    $("#risk").text('Risk is '+risk);
    $("#cost").text('Cost is '+cost);
    createGraph(date,cost,risk);
}
function createGraph(date,cost,risk){

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
 { type: "line", name: "Risk(%) ", showInLegend: true, dataPoints : dps1},
 { type: "line", name: "Productivity cost($ million) ", showInLegend: true, dataPoints : dps2}
 ]
 // end of data for 2 line graphs

 }); // End of new chart variable

 chart.render();

}
