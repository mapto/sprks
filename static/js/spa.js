/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 18.07.13
 * Time: 10:52
 * To change this template use File | Settings | File Templates.
 */
    $("#home_page").css("display", "block");

    //REGISTER script
    $(".register_page").click('click', function(e){
            $("#register_page").css("display", "block");
    });

    //LOGIN script
    $(".login_page").click('click', function(e){
            $("#login_page").css("display", "block");
    });

    //PSWD RECOVER script
    $(".password_recover_page").click('click', function(e){
            $("#password_recover_page").css("display", "block");
    });

    //PSWD CHANGE script
    $(".password_change_page").click('click', function(e){
            $("#password_change_page").css("display", "block");
    });

    //INCIDENT script
    $(".incident_page").click('click', function(e){
            initIncident();
            $("#incident_page").css("display", "block");
    });

    //INTRO script
    $(".intro_page").click('click', function(e){
            $("#intro_page").css("display", "block");
    });

    //PROFILE script
    $(".profile_page").click('click', function(e){
            $("#profile_page").css("display", "block");
            initProfile();
    });

    //POLICY script
    $(".policy_page").click('click', function(e){
            $("#policy_page").css("display", "block");
            initPolicy();
    });
    //SCORE script
    $(".score_page").click('click', function(e){
            $("#score_page").css("display", "block");
            initScore();
    });
