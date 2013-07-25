/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 05.07.13
 * Time: 14:51
 * To change this template use File | Settings | File Templates.
 */
var score_obj;
function initScore(){
    send_request(); //request scores, write them to score_obj global variable
    console.log(score_obj);
    //create accordion score representation
    //new Fx.Accordion(accordion, '#accordion h2', '#accordion .content');
    $('#accordion').accordion({
        heightStyle: "content",
        icons: null
    });
    climbLadder("risk");
    climbLadder("cost");
    $("#avg_risk").text(score_obj.avg_risk);
    $("#avg_pc").text(score_obj.avg_pc);
    console.log("Score initialized...");
    congratulate_first();
}

function send_request(){
    var request = jQuery.ajax({
        url: "/score_rest",
        type: "GET",
        async : false,

        success : function(score) {
            score_obj = JSON.parse(score.toString());
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
    return false;
}

// Ladder is "risk" or "cost"
function climbLadder(ladder) {
    console.log("entered climb");
    // scores:
    var own = getScore("Own", ladder);
    var contender = getScore("Contender", ladder);
    var best = getScore("Best", ladder);

    if (own["value"] == best["value"]) {
        putOnLadder(ladder, 1, getUsername());
        putOnLadder(ladder, 2, "Contender");
        putOnLadder(ladder, 3, "Average");
    } else {  // own < best not possible
        putOnLadder(ladder, 1, "Best");
        if (own["value"] <= contender["value"]) {
            putOnLadder(ladder, 2, getUsername());
            putOnLadder(ladder, 3, "Contender")
        } else {
            putOnLadder(ladder, 3, getUsername());
            putOnLadder(ladder, 2, "Contender");
        }
    }
}

function putOnLadder(ladder, step, name) {
    // score contains "value", "rank" and "when"
    // ladder is "risk" or "cost"
    score = getScore(name, ladder);
    $("#" + ladder + "_s" + step).text(name + ', ' + score["value"]);
    $("#" + ladder + "_r" + step).text(score["rank"]);
    $("#" + ladder + "_w" + step).text(score["when"]);

}

function getScore(user, type) {
        switch (user) {
            case "Best":
            case "Contender":
            case "Own":
            case "Average":
                call = "get" + user + capitalise(type); // user is already capitalized
                break;
            default:
                call = "getOwn" + capitalise(type);
        }
        fn = window[call];
//        console.log("user " + user + ", ladder " + type + ", call " + call + ", value " + fn()["value"]);
        return fn();
    }

// utility function
    function capitalise(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

// These values are set server-side and appear to client as json.
    function getOwnRisk() {
        return {"value": score_obj.b_u_risk, "rank": score_obj.b_u_risk_rank, "when": score_obj.b_u_risk_date};
    }
    function getOwnCost() {
        return {"value": score_obj.b_u_cost, "rank": score_obj.b_u_cost_rank, "when": score_obj.b_u_cost_date};
    }
    function getContenderRisk() {
        return {"value": score_obj.c_risk, "rank": score_obj.c_risk_rank, "when": score_obj.c_risk_when};
    }
    function getContenderCost() {
        return {"value": score_obj.c_pc, "rank": score_obj.c_pc_rank, "when": score_obj.c_pc_when};
    }
    function getBestRisk() {
        return {"value": score_obj.b_risk, "rank": 1, "when": score_obj.b_risk_when};
    }
    function getBestCost() {
        return {"value": score_obj.b_pc, "rank": 1, "when": score_obj.b_pc_when};
    }
    function getAverageRisk() {
        return {"value": score_obj.avg_risk, "rank": "", "when": ""};
    }
    function getAverageCost() {
        return {"value": score_obj.avg_pc, "rank": "", "when": ""};
    }











//congratulations popup (if a user is first
function congratulate_first(){
    var text = '';
    if( getOwnRisk().value === getBestRisk().value || getOwnCost().value === getBestCost().value){
       text = 'Congratulations, you got the best';
     if( getOwnRisk().value === getBestRisk().value){
       text = text+ ' Risk';
     }
     if (getOwnCost().value === getBestCost().value){
       if(getOwnRisk().value === getBestRisk().value){text = text+' and';}
       text = text+ ' Cost';
     }

     $("#congratulate").text(text);
     $("#congratulate").show();
     $('#congratulate').delay(2500).fadeOut();
    }


}






