// Global and init scripts for whole SPA
pageModel = {
    currentPage: ko.observable('')
}

var policyUpdate = [];
var policies_array = {};

$(function(){

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

// highlight active button(scores/story/policy)
function highlightActiveButton() {

    switch (title) {
        case "score":
            if ($(".score_page").css("display") === "block") {
                css_class = "score";
            }
            break;
        case "intro":
            css_class = "intro";
            break;
        case "profile":
            css_class = "profile";
            break;
        case "incident":
            if ($(".incident_page").css("display") === "block") {
                css_class = "incident";
            }
            break;
        case "policy":
            css_class = "policy";
            break;
        default:
            css_class = "";
    }

    deactivateButtons();

    $("." + css_class + "_page").css("background-color", "#C10000");
    $("." + css_class + "_page").css("color", "#fff");
    $("." + css_class + "_page").css("cursor", "default");

}

function deactivateButtons() {
    $('.intro_page').removeAttr('style');
    if ($(".score_page").css("display") === "block") {
        $('.score_page').removeAttr('style');
    }
    if ($(".incident_page").css("display") === "block") {
        $('.incident_page').removeAttr('style');
    }
    $('.profile_page').removeAttr('style');
    $('.policy_page').removeAttr('style');
}

function hideOtherPages(page_name) {
        $(".pages").each(function () {
            if ($(this).attr('id') !== page_name) {
                $(this).css("display", "none");
            }
        });
    }

function clearProfile() {
    $(".profile_table").each(function () {    //clear table
        this.remove();
    });
    $('#chartContainer').empty();           //clear graph
}

/*****Display/hide pages *****/
$('a').click('click', function () {
    var page = $(this).attr('class');
    if ((page.substr(page.length - 4)) === 'page') { //check if the link clicked if a page button
        hideOtherPages(page);

        $("#" + page).css("display", "block");
        if (page === 'profile_page') {
            clearProfile();
            initProfile();
        }
        if (page === 'score_page') {
            initScore();
        }

        title = page.substr(0, page.length - 5);
        highlightActiveButton();
        $(".main-body").show();

        get_score_frame();
    }
});

$("#close_btn").click(function(){
    $(".main-body").hide();
    $(".pages").hide();
    deactivateButtons();
    pageModel.currentPage('');
});

$(function(){
    ko.applyBindings(pageModel, document.getElementById('menu'));
})