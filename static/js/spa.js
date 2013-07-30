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

$('a').click('click', function () {
    var page = $(this).attr('class');
    if ((page.substr(page.length - 4)) === 'page') { //check if the link clicked if a page button
        hideOtherPages(page);

        $("#" + page).css("display", "block");
        if (page === 'policy_page') {
            initPolicy();
        }
        if (page === 'incident_page') {
            initIncident();
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
    $(".main-body").css("display", "none");
    $(".pages").each(function(){
        $(this).css("display", "none");
    });
    deactivateButtons();
});

$(function () {

    resume();

    if (getUserID() > 0) {
        $(".main-body").css("display", "block");
        $("#intro_page").css("display", "block");
        title = 'intro';
        highlightActiveButton();

        get_score_frame();
    } else {
        $(".main-body").css("display", "block");
        $("#home_page").css("display", "block");
    }

})