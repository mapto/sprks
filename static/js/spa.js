// Global and init scripts for whole SPA

var policyUpdate = [];
var policies_array = {};

$(function(){

    if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
        $(".risk-menu").css("display", "none");
    } else {
        $(".risk-menu").css("display", "block");
    }

    $(document).click(function () {
        if ($("#risk_menu").text() == '' || $("#cost_menu").text() == '') {
            $(".risk-menu").css("display", "none");
        } else {
            $(".risk-menu").css("display", "block");
        }
    });

    $('#pause').click(function() {
        $('.target').removeAttr('disabled');
        $('#apply').removeAttr('disabled');
        pauseInterval();

    });

    $('#forward').click(function() {
        $('.target').attr('disabled', 'disabled');
        $('#apply').attr('disabled', 'disabled');
        startTimer(500);
    })

    $('.target').change(function(){
        window.id_elem = $(this).closest($(".qn")).attr('id');
    })
    $('#play').click(function () {
        $('.target').attr('disabled', 'disabled');
        $('#apply').attr('disabled', 'disabled');
        startTimer(3000);
    });

    console.log("Private decoration initialized...");
});

// Decides whether to show score button
// If different elements of the interface need to show up in later turns,
// this could be done here

// highlight active button(scores/story/policy)
function highlightActiveButton() {

    switch (title) {
        case "score":
            if($(".score_page").css("display")=== "block"){ css_class = "score";}
            break;
        case "intro":
            css_class = "intro";
            break;
        case "profile":
            css_class = "profile";
            break;
        case "incident":
            if($(".incident_page").css("display")=== "block"){ css_class = "incident";}
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


//time-control buttons active css
$('#play').click(function() {
   $(this).parent().addClass('active');
   $('#pause').parent().removeClass('active');
   $('#forward').parent().removeClass('active');
});
$('#pause').click(function() {
   $(this).parent().addClass('active');
   $('#play').parent().removeClass('active');
   $('#forward').parent().removeClass('active');
});
$('#forward').click(function() {
   $(this).parent().addClass('active');
   $('#play').parent().removeClass('active');
   $('#pause').parent().removeClass('active');
});


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
        if (page === 'policy_page') {

        }
        if (page === 'incident_page') {

        }
        if (page === 'profile_page') {
            clearProfile();
            initProfile();
        }
        if (page === 'score_page') {
            initScore();
        }

        title = page.substr(0, page.length - 5);
        highlightActiveButton();
        $(".main-body").css("display", "block");

        get_score_frame();
    }
});

$("#close_btn").click('click', function(){
    $(".main-body").hide();
    $(".pages").hide();
    deactivateButtons();
});
