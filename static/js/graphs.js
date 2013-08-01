/**
 * Created with PyCharm.
 * User: mruskov
 * Date: 22/06/13
 * Time: 13:25
 * To change this template use File | Settings | File Templates.
 */
function submit_alternatives_request() {
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
        console.log("id");
        console.log(id_tmp);
        console.log("next");
        console.log(next);
        console.log("new");
        console.log(new_policy);

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
            initialize_graphs(policy_costs_risks);
        },
        error: function (response) {
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