/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 22/06/13
 * Time: 13:25
 * To change this template use File | Settings | File Templates.
 */
function submitAlternativesRequest() {
    statusUpdating();
    var msgs = {'context': {'employees': [], 'locations': [], 'devices': []}, 'data': []};
    var new_policy = {};
    var msg = {};
    var risk = [];
    var cost = [];
    var ids = [];

    msg.id = $(this).closest($(".qn")).attr('id'); //get the id of a question with changed option

    $("#employee").find('input').each(function() {
        if ($(this).is(':checked')) {
            var next = $(this).val();
            msgs['context']['employees'].push(next);
        }
    });

    $("#location").find('input').each(function() {
        if ($(this).is(':checked')) {
            var next = $(this).val();
            msgs['context']['locations'].push(next);
        }
    });

    $("#device").find('input').each(function() {
        if ($(this).is(':checked')) {
            var next = $(this).val();
            msgs['context']['devices'].push(next);
        }
    });

    new_policy.bdata = $('select[name="bdata"]').find('option:selected').val();
    new_policy.pdata = $('select[name="pdata"]').find('option:selected').val();
    new_policy.plen = $('input[name="plen"]:checked').val();
    new_policy.psets = $('input[name="psets"]:checked').val();
    new_policy.pdict = $('input[name="pdict"]').is(':checked') ? 1 : 0;
    new_policy.precovery = $('input[name="precovery"]').is(':checked') ? 1 : 0;
    new_policy.phist = $('input[name="phist"]:checked').val();
    new_policy.prenew = $('input[name="prenew"]:checked').val();
    new_policy.pattempts = $('input[name="pattempts"]:checked').val();
//    msg.data = JSON.stringify(new_policy);

//    msgs.push(msg);

    $(".qn").each(function (i) { //iteration accross questions
        var id_tmp = $(this).attr('id');
        next = get_range(new_policy, id_tmp);
        /*
        console.log("id");
        console.log(id_tmp);
        console.log("next");
        console.log(next);
        console.log("new");
        console.log(new_policy);
        */
        msgs['data'] = msgs['data'].concat(next);
    });
//    msgs = msgs.concat(get_range(new_policy, msg.id));
    // console.log(msgs.concat(get_range(new_policy, "plen")));
    var request = $.ajax({
        url: "/score/multiple",
        type: "POST",
        async: true,
        data: JSON.stringify(msgs),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (policy_costs_risks) {
            statusReady();
            initialize_graphs(policy_costs_risks);
        },
        error: function (response) {
            statusReady();
            console.log("fail: " + response.responseText);
        }
    });
    return false;

}

function create_variation(policy, id, value) {
    var new_policy = {};
    for (var key in policy) {
        new_policy[key] = policy[key];
    }
    new_policy[id] = value;

    return new_policy;
}

function get_range(policy, id) {
    var msgs = [];
    $(document).find("#" + id).find('input,option').each(function (i) {
        var new_policy = create_variation(policy, id, this.value);
        var msg = {};

        msg['id'] = id + this.value;
        msg.data = JSON.stringify(new_policy);
        msgs.push(msg);

    });
    return msgs;
}
function initialize_graphs(policy_costs_risks) { //id examples: plen, psets, pdict, etc.
    console.log(policy_costs_risks);
    var graph_id = {};
    dps_risk = {};
    dps_cost = {};

    $(".qn").each(function (i) {
        dps_risk[$(this).closest($(".qn")).attr('id')] = [];//initializing dps
        dps_cost[$(this).closest($(".qn")).attr('id')] = [];//initializing dps
        graph_id[$(this).closest($(".qn")).attr('id')] = "graph_" + [$(this).closest($(".qn")).attr('id')]; //assigning graph ids like graph_id.plen = "graph_plen"
        console.log(graph_id);
    });

    $(policy_costs_risks).each(function (i) {
        if (this.id.replace(/[a-z]+/, '') != '') {//skip ids without value numbers to avoid duplicate data (e.g. plen)
            var new_string = this.id.replace(/[0-9]+/, ''); // removing numbers from plen0 etc.
            tmpRisk = {label: this.id, y: this.risk};
            tmpCost = {label: this.id, y: this.cost};
            dps_risk[new_string].push(tmpRisk);
            dps_cost[new_string].push(tmpCost);
        }
    });
    console.log("Initializing graphs details(ids, risks, costs)...");
//    console.log(graph_id);
//    console.log(dps_risk);
//    console.log(dps_cost);

    display_graphs(graph_id, dps_risk, dps_cost);
}

function display_graphs(graph_id, dps_risk, dps_cost) {
    $('.graph').each(function(){
        $('#'+this.getAttribute('id')).empty();
    });
    $(".qn").each(function (i) {


        var chart = new CanvasJS.Chart(graph_id[$(this).closest($(".qn")).attr('id')], { //processing graph for each question
            title: {},
            axisX: {},
            axisY: {
                minimum: 0.0,
                maximum: 1.0
            },
            // begin data for 2 line graphs. Note dps1 and dps2 are
            //defined above as a json object. See http://www.w3schools.com/json/
            data: [
                { type: "line", color: "#c24642", name: "Risk", showInLegend: true, dataPoints: dps_risk[$(this).closest($(".qn")).attr('id')]},
                { type: "line", color: "#499249", name: "Cost", showInLegend: true, dataPoints: dps_cost[$(this).closest($(".qn")).attr('id')]}
            ]
            // end of data for 2 line graphs

        }); // End of new chart variable

        chart.render();

    });

}

var data = [
    {label: "no restriction" , risk: .99, cost: .01},
    {label: "min 6 chars" , risk: .6 , cost: .2 },
    {label: "min 8 chars" , risk: .3 , cost: .3 },
    {label: "min 10 chars", risk: .3 , cost: .5 },
    {label: "min 12 chars", risk: .7 , cost: .8 }
];

function select(i) {
    d3.select("svg").remove();
//    console.log("selected " + i);
    drawD3chart(data, i);
}

function clearD3chart() {
    var vis = d3.select("#myChart").remove()
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h)

}
/*
function lineChart(root, data, selected) {
    var yLabels = ["very low", "low", "average", "high", "very high"],
    margin = {top: 10, right: 50, bottom: 30, left: 40},
    w = 400,
    h = 300,
    y = d3.scale.linear().domain([0, 1]).range([0 + margin.bottom, h - margin.top]),
    x = d3.scale.linear().domain([0, data.length]).range([0 + margin.left, w - margin.right]);

    console.log(selected + " " + x(selected) + " " + y(selected));

    var vis = d3.select(root)
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h)

    var chart = vis.append("svg:g")
        .attr("transform", "translate(0, " + h + ")"); // 200 is height

    var riskLine = d3.svg.line()
        .x(function(d,i) { return x(i); })
        .y(function(d) { return -1 * y(d.risk); })

    var costLine = d3.svg.line()
        .x(function(d,i) { return x(i); })
        .y(function(d) { return -1 * y(d.cost); })

    chart.append("svg:rect")
        .attr("x", x(selected) - 40)
        .attr("y", -1 * (h - margin.top))
        .attr("width", 80)
        .attr("height", h - margin.top)
        .attr("class", "highlight");

    chart.append("svg:path")
        .attr("d", riskLine(data))
        .attr("class", "risk-line");

    chart.append("svg:path")
        .attr("d", costLine(data))
        .attr("class", "cost-line");

     chart.selectAll(".cost-node")
        .data(data)
        .enter().append("svg:circle")
        .attr("class", "cost-node")
        .attr("cx", function(d,i) { return x(i); })
        .attr("cy", function(d,i) { return -1 * y(d.cost); })
        .attr("r", function(d,i) { return i == selected ? 6 : 3})
        .attr("title", function(d,i){ return y(d.risk);})
        .on("click", function(d,i){ select(i);})

     chart.selectAll(".risk-node")
        .data(data)
        .enter().append("svg:circle")
        .attr("class", "risk-node")
        .attr("cx", function(d,i) { return x(i); })
        .attr("cy", function(d,i) { return -1 * y(d.risk); })
        .attr("r", function(d,i) { return i == selected ? 6 : 3})
        .attr("title", function(d,i){ y(d.risk);})
        .on("click", function(d,i){ select(i);})

   // x axis
    chart.append("svg:line")
        .attr("x1", x(0))
        .attr("y1", -1 * y(0))
        .attr("x2", x(data.length - 1))
        .attr("y2", -1 * y(0))

    // y axis
    chart.append("svg:line")
        .attr("x1", x(0))
        .attr("y1", -1 * y(0))
        .attr("x2", x(0))
        .attr("y2", -1 * y(1))

    chart.selectAll(".xLabel")
        .data(x.ticks(data.length))
        .enter().append("svg:text")
        .attr("class", "xLabel option")
        .text(function(d) { return data[d].label })
        .attr("x", function(d) { return x(d) })
        .attr("y", 0)
        .attr("text-anchor", "middle")
        .on("click", function(d,i){ select(i);})
        .attr("font-weight", function(d,i) { return i == selected ? "bold" : "normal"})

    chart.selectAll(".yLabel")
        .data(y.ticks(6))
        .enter().append("svg:text")
        .attr("class", "yLabel")
        .text(String)
        .attr("x", 0)
        .attr("y", function(d) { return -1 * y(d) })
        .attr("text-anchor", "right")
        .attr("dy", 4)

    chart.selectAll(".xTicks")
        .data(x.ticks(data.length))
        .enter().append("svg:line")
        .attr("class", "xTicks")
        .attr("x1", function(d) { return x(d); })
        .attr("y1", -1 * y(0))
        .attr("x2", function(d) { return x(d); })
        .attr("y2", -1 * y(-0.05))

    chart.selectAll(".yTicks")
        .data(y.ticks(4))
        .enter().append("svg:line")
        .attr("class", "yTicks")
        .attr("y1", function(d) { return -1 * y(d); })
        .attr("x1", x(-0.05))
        .attr("y2", function(d) { return -1 * y(d); })
        .attr("x2", x(0))

}
*/
function drawD3chart(root, data, selection) {
    barChart(root, data, selection);
}

function barChart(root, data, selection) {
    // from: http://hdnrnzk.me/2012/07/04/creating-a-bar-graph-using-d3js/
//    var scale = ["very low", "low", "average", "high", "very high"],
    var scale = ["low", "average", "high"];
    var vis = d3.select(root);
    var margin = {top: 20, right: 10, bottom: 20, left: 90},
    items = data.length,
    w = vis.width,
    h = vis.height,
    inner_w = w - margin.left - margin.right,
    bar_height = (h - margin.top - margin.bottom) / items,
    y = d3.scale.linear().domain([0, items]).range([0 + margin.top, h - margin.bottom]),
    x = d3.scale.linear().domain([0, 1]).range([0 + margin.left, w - margin.right]);

    vis.append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    var bg = vis.append("svg:g")
        .attr("class", "background");

    var chart = vis.append("svg:g");
//        .attr("transform", "translate(100, 10)");

    bg.selectAll(".xTicks")
        .data(x.ticks(6))
        .enter().append("svg:line")
        .attr("class", "xTicks")
        .attr("x1", function(d,i) {return x(d) ; })
        .attr("y1", y(0))
        .attr("x2", function(d,i) { return x(d); })
        .attr("y2", y(items - 1/3));

    bg.selectAll(".buttons")
        .data(data)
        .enter().append("svg:rect")
        .attr("x", 0)
        .attr("y", function(d,i) { return y(i) - 4; })
        .attr("width", w)
        .attr("height", bar_height)
        .attr("class", function(d,i) { return i == selection ? "highlight" : "buttons";} )
        .on("click", function(d,i){ select(i);});

    bg.selectAll(".xLabel")
        .data(x.ticks(scale.length))
        .enter().append("svg:text")
        .attr("class", "xLabel")
        .text(function(d,i) { return scale[i] })
        .attr("x", function(d,i) { return x(d) - 5 * (i - 1);}) //i * ((inner_w)/ scale.length) + 25})
        .attr("y", margin.top / 2)
        .attr("text-anchor", "middle");

    bg.append("svg:text")
       .text("risk")
       .attr("x", x(1/3))
       .attr("y", h - margin.bottom + 6)
       .attr("class", "risk-node")
       .attr("text-anchor", "middle");

    bg.append("svg:text")
       .text("cost")
       .attr("x", x(2/3))
       .attr("y", h - margin.bottom + 6)
       .attr("class", "cost-node")
       .attr("text-anchor", "middle");

/*
    chart.append("svg:rect")
        .attr("x", 0)
        .attr("y", y(selection) - 3)
        .attr("width", w)
        .attr("height", bar_height)
        .attr("class", "highlight");
*/
    chart.selectAll(".ylabel")
      .data(data)
      .enter().append("svg:text")
      .attr("x", 0 )
      .attr("y", function(d,i){ return y(i + 1/6); } )
//      .attr("dx", margin.left * 2/3)
      .attr("dy", bar_height / 3 )
      .attr("text-anchor", "start")
      .text(function(d,i){ return d.label } )
      .attr("class", "option")
      .on("click", function(d,i){ select(i);});

    chart.selectAll(".risk-node")
       .data(data)
       .enter().append("svg:rect")
       .attr("x", x(0))
       .attr("y", function(d, i) { return y(i + 0/3); })
       .attr("width", function(d) { return x(d.risk) - x(0); })
       .attr("height", bar_height * 1/3)
       .attr("class", "risk-node")
       .on("click", function(d,i){ select(i);});

    chart.selectAll(".cost-node")
       .data(data)
       .enter().append("svg:rect")
       .attr("x", x(0))
       .attr("y", function(d, i) { return y(i + 1/3); })
       .attr("width", function(d) { return x(d.cost) - x(0); })
       .attr("height", bar_height * 1/3)
       .attr("class", "cost-node")
       .on("click", function(d,i){ select(i);});
}