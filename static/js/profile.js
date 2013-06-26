/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 25.06.13
 * Time: 16:27
 * To change this template use File | Settings | File Templates.
 */
function init() {
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

    createGraph(date,cost,risk,json);

    for(var k in json)
    {

        if(k>0 && (json[k-1].risk != json[k].risk)){ //if risk changed
            console.log('prev '+json[k-1].risk + 'curr '+ json[k].risk);
        }else{
            console.log(k+' '+json[k].risk);
        }


    }
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
