function updateScoreFrame() {

    $.ajax({
        url: "api/score_frame",
        type: "GET",
        success: function (data) {
            if (data && data !== 'None') {
                var score_frame = [];
                score_frame.push(data[data.length - 1]);
                score_frame.push(data[data.length - 2]);
                $(score_frame).each(function () {
                    if (this.score_type === '1') {
                        pageModel.currentRisk(verboseScore(this.score_value));
                    } else if (this.score_type === '2') {
                        pageModel.currentCost(verboseScore(this.score_value));
                    }
                });
            }
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
}