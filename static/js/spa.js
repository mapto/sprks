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

$('a').click('click', function () {
    var page = $(this).attr('class');
    if ((page.substr(page.length - 4)) === 'page') { //check if the link clicked if a page button

        pageModel.currentPage(page);
    }
});

$("#close_btn").click(function(){
    pageModel.currentPage('');
});

$(function(){
$(".main-body").show();
    ko.applyBindings(pageModel);

    pageModel.currentPage.subscribe(function (currentPage) {
        $("#main-body").show();
        switch (currentPage) {
            case '':
                $("#main-body").hide();
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
                if ($(".incident_page").css("display") === "block") {
                    css_class = "incident";
                }
                break;
            case 'profile_page':
                clearProfile();
                initProfile();
                break;
            case 'score_page':
                initScore();
                if ($(".score_page").css("display") === "block") {
                    css_class = "score";
                }
                break;
        }
    });
});