var score_obj;
function initScore(){
    retrieveScores(); //request scores, write them to score_obj global variable
    //create accordion score representation
    //new Fx.Accordion(accordion, '#accordion h2', '#accordion .content');
    $('#accordion').accordion({
        heightStyle: "content",
        icons: null
    });
    climbLadder("risk");
    climbLadder("cost");
    $("#avg_risk").text(parseFloat(score_obj.avg_risk).toFixed(2));
    $("#avg_pc").text(parseFloat(score_obj.avg_pc).toFixed(2));
    console.log("Score initialized...");
    congratulate_first();

}

function retrieveScores(){
    $.ajax({
        url: "api/score",
        type: "GET",
        success : function(score) {
            score_obj = score;
        },
        error: function(response) {
            console.log("fail: " + response.responseText);
        }
    });
}

// Ladder is "risk" or "cost"
function climbLadder(ladder) {
    // scores:
    var own = getScore("Own", ladder);
    var contender = getScore("Contender", ladder);
    var best = getScore("Best", ladder);

    if (own["value"] == best["value"]) {
        putOnLadder(ladder, 1, loginModel.username());
        putOnLadder(ladder, 2, "Contender");
        putOnLadder(ladder, 3, "Average");
    } else {  // own < best not possible
        putOnLadder(ladder, 1, "Best");
        if (own["value"] <= contender["value"]) {
            putOnLadder(ladder, 2, loginModel.username());
            putOnLadder(ladder, 3, "Contender")
        } else {
            putOnLadder(ladder, 3, loginModel.username());
            putOnLadder(ladder, 2, "Contender");
        }
    }
}

function putOnLadder(ladder, step, name) {
    // score contains "value", "rank" and "when"
    // ladder is "risk" or "cost"
    score = getScore(name, ladder);
    switch (name) {
            case "Best":
                $("#" + ladder + "_s" + step).text('anonymous (best) ,');
                $("#" + ladder + "_w" + step).text(format_date(new Date(score["when"])));
                break;
            case "Contender":
                $("#" + ladder + "_s" + step).text('anonymous (contender) ,');
                $("#" + ladder + "_w" + step).text(format_date(new Date(score["when"])));
                break;
            case "Average":
                $("#" + ladder + "_s" + step).text('anonymous (average) ,');
                break;
            default:
                $("#" + ladder + "_s" + step).text(name+' (player) ,');
                $("#" + ladder + "_w" + step).text(format_date(new Date(score["when"])));
        }
    $("#" + ladder + "_s" + step+"_v1").text(score["value"]);
    $("#" + ladder + "_s" + step+"_v2").text(score["value_2"]);
    $("#" + ladder + "_r" + step).text(score["rank"]);



    //Styling ranking ladder
    //appropriate height
    if(step=='1'){
        var height = 200/score["rank"];
        $('#'+ladder.substr(0,1)+'_first').css("height", height+"px");
        $('#'+ladder.substr(0,1)+'_first').css("min-height", "40px");
    }else if(step=='2'){
        var height = 200/score["rank"];
        $('#'+ladder.substr(0,1)+'_second').css("height", height+"px");
         $('#'+ladder.substr(0,1)+'_second').css("min-height", "40px");
    }else if(step=='3'){
        var height = 200/score["rank"];
        $('#'+ladder.substr(0,1)+'_third').css("height", height+"px");
         $('#'+ladder.substr(0,1)+'_third').css("min-height", "40px");
    }

    //TODO appropriate color, is current schema intuitive enough?
    if($('#'+ladder.substr(0,1)+'_first').css("height")!='0px'&&
       $('#'+ladder.substr(0,1)+'_second').css("height")!='0px'&&
       $('#'+ladder.substr(0,1)+'_first').css("height")==$('#'+ladder.substr(0,1)+'_second').css("height")){
            $('#'+ladder.substr(0,1)+'_second').css("background-image", $('#'+ladder.substr(0,1)+'_first').css("background-image"));
            $('#'+ladder.substr(0,1)+'_third').css("border", $('#'+ladder.substr(0,1)+'_second').css("border"));
    }
    if($('#'+ladder.substr(0,1)+'_third').css("height")!='0px'&&
       $('#'+ladder.substr(0,1)+'_second').css("height")!='0px'&&
       $('#'+ladder.substr(0,1)+'_third').css("height")==$('#'+ladder.substr(0,1)+'_second').css("height")){
            $('#'+ladder.substr(0,1)+'_third').css("background-image", $('#'+ladder.substr(0,1)+'_second').css("background-image"));
            $('#'+ladder.substr(0,1)+'_third').css("border", $('#'+ladder.substr(0,1)+'_second').css("border"));
    }
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
        return {"value": score_obj.b_u_risk, "rank": score_obj.b_u_risk_rank, "when": score_obj.b_u_risk_date, "value_2": score_obj.b_u_risk_cost};
    }
    function getOwnCost() {
        return {"value": score_obj.b_u_cost, "rank": score_obj.b_u_cost_rank, "when": score_obj.b_u_cost_date, "value_2": score_obj.b_u_cost_risk};
    }

    function getContenderRisk() {
        return {"value": score_obj.c_risk, "rank": score_obj.c_risk_rank, "when": score_obj.c_risk_when, "value_2": score_obj.c_risk_cost};
    }
    function getContenderCost() {
        return {"value": score_obj.c_pc, "rank": score_obj.c_pc_rank, "when": score_obj.c_pc_when, "value_2": score_obj.c_pc_risk};
    }
    function getBestRisk() {
        return {"value": score_obj.b_risk, "rank": 1, "when": score_obj.b_risk_when, "value_2": score_obj.b_risk_cost};
    }
    function getBestCost() {
        return {"value": score_obj.b_pc, "rank": 1, "when": score_obj.b_pc_when, "value_2":score_obj.b_pc_risk};
    }
    function getAverageRisk() {
        return {"value": parseFloat(score_obj.avg_risk).toFixed(2), "rank": "", "when": "", "value_2": parseFloat(score_obj.avg_pc).toFixed(2)};
    }
    function getAverageCost() {
        return {"value": parseFloat(score_obj.avg_pc).toFixed(2), "rank": "", "when": "", "value_2": parseFloat(score_obj.avg_risk).toFixed(2)};
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