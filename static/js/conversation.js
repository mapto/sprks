 $(document).ready(function(){

        $("#interview1").on('click', function(e){
            if( $("#quote1").css("display")=="block"){
                $("#quote1").css("display", "none");
            }else{
                $("#quote1").css("display", " block");
                $("#quote2").css("display", " none");
                $("#quote3").css("display", " none");
                 e.stopPropagation();
            }

        });
        $("#interview2").on('click', function(e){
            if( $("#quote2").css("display")=="block"){
                $("#quote2").css("display", "none");
            }else{
                $("#quote2").css("display", " block");
                $("#quote1").css("display", " none");
                $("#quote3").css("display", " none");
                 e.stopPropagation();
            }
        });
        $("#interview3").on('click', function(e){
            if( $("#quote3").css("display")=="block"){
                $("#quote3").css("display", "none");
            }else{
                $("#quote3").css("display", " block");
                $("#quote2").css("display", " none");
                $("#quote1").css("display", " none");
                e.stopPropagation();
            }
        });

    $(document).click(function(){
         $("#quote1").css("display", "none");
         $("#quote2").css("display", "none");
         $("#quote3").css("display", "none");
    });

    });
