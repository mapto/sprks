// Global and init scripts for whole SPA
pageModel = {
    currentPage: ko.observable('home_page'),
    currentRisk: ko.observable(''),
    currentCost: ko.observable(''),
    timeline: timelineModel,
    status: statusModel,
    map: charactersModel,
    register: registerModel,
    login: loginModel,
    passwordChange: passwordChangeModel,
    passwordRecover: passwordRecoverModel,
    incident: incidentModel,
    report: reportModel
};

var policyUpdate = [];
var policies_array = {};

$(function () {

    $('.target').change(function(){
        window.id_elem = $(this).closest($(".qn")).attr('id');
    });

    console.log("Private decoration initialized...");
});

function clearProfile() {
    $(".profile_table").each(function () {    //clear table
        this.remove();
    });
    $('#chartContainer').empty();           //clear graph
}

$(function(){
    ko.applyBindings(pageModel);

    pageModel.currentPage.subscribe(function (currentPage) {
        switch (currentPage) {
            case 'profile_page':
                clearProfile();
                get_profile();
                break;
            case 'policy_page':
                submitAlternativesRequest();
                break;
            case 'score_page':
                initScore();
                break;
        }
    });
});