/**
 * Created with PyCharm.
 * User: Жанеля
 * Date: 18.07.13
 * Time: 10:52
 * To change this template use File | Settings | File Templates.
 */

    if(getUserID() > 0) {
        $(".main-body").css("display", "block");
        $("#intro_page").css("display", "block");
    }else{
        $(".main-body").css("display", "block");
        $("#home_page").css("display", "block");
    }



    $('a').click('click', function(){
       var page = $(this).attr('class');
       if((page.substr(page.length-4))==='page'){ //check if the link clicked if a page button
            hideOtherPages(page);
            $("#"+page).css("display", "block");
            if(page==='policy_page'){initPolicy();}
            if(page==='incident_page'){initIncident();}
            if(page==='profile_page'){initProfile();}
            if(page==='score_page'){initScore();}

            $(".main-body").css("display", "block");
       }
    });

    $("#close_btn").click('click', function(){
        $(".main-body").css("display", "none");
        $(".pages").each(function(){
            $(this).css("display", "none");
        });
    });

    function hideOtherPages(page_name){
        $(".pages").each(function(){
            if($(this).attr('id')!==page_name){
                $(this).css("display", "none");
            }
        });
    }

