// Global and init scripts for whole SPA
pageModel = {
    currentPage: ko.observable('home_page'),
    timeline: timelineModel,
    statusBar: statusBarModel,
    map: charactersModel,
    register: registerModel,
    login: loginModel,
    passwordChange: passwordChangeModel,
    passwordRecover: passwordRecoverModel,
    incident: incidentModel
};

var policyUpdate = [];
var policies_array = {};

$(function () {
    if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
        $(".risk-menu").hide();
    } else {
        $(".risk-menu").show();
    }

    $(document).click(function () {
        if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
            $(".risk-menu").hide();
        } else {
            $(".risk-menu").show();
        }
    });

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
            case '':
                break;
            case 'home_page':
                break;
            case 'register_page':
                break;
            case 'login_page':
                break;
            case 'password_recover_page':
                break;
            case 'password_change_page':
                break;
            case 'intro_page':
                break;
            case 'policy_page':
                break;
            case 'incident_page':
                break;
            case 'profile_page':
                clearProfile();
                get_profile();
                break;
            case 'score_page':
                initScore();
                break;
        }
    });
});