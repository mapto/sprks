 $(document).ready(function(){

        $("#andydiv").on('click', function(e){
            if( $("#andyquote").css("display")=="block"){
                $("#andyquote").css("display", "none");
            }else{
                $("#andyquote").css("display", " block");
                $("#izaquote").css("display", " none");
                $("#kevquote").css("display", " none");
                $("#susquote").css("display", " none");
                $("#drkquote").css("display", " none");
                $("#helquote").css("display", " none");
                 e.stopPropagation();
            }

        });
        $("#izadiv").on('click', function(e){
            if( $("#izaquote").css("display")=="block"){
                $("#izaquote").css("display", "none");
            }else{
                $("#izaquote").css("display", " block");
                $("#andyquote").css("display", " none");
                $("#kevquote").css("display", " none");
                $("#susquote").css("display", " none");
                $("#drkquote").css("display", " none");
                $("#helquote").css("display", " none");

                 e.stopPropagation();
            }
        });
        $("#kevdiv").on('click', function(e){
            if( $("#kevquote").css("display")=="block"){
                $("#kevquote").css("display", "none");
            }else{
                $("#kevquote").css("display", " block");
                $("#izaquote").css("display", " none");
                $("#andyquote").css("display", " none");
                $("#susquote").css("display", " none");
                $("#drkquote").css("display", " none");
                $("#helquote").css("display", " none");
                e.stopPropagation();
            }
        });
        $("#susdiv").on('click', function(e){
            if( $("#susquote").css("display")=="block"){
                $("#susquote").css("display", "none");
            }else{
                $("#susquote").css("display", " block");
                $("#andyquote").css("display", " none");
                $("#izaquote").css("display", " none");
                $("#kevquote").css("display", " none");
                $("#drkquote").css("display", " none");
                $("#helquote").css("display", " none");
                e.stopPropagation();
            }
        });
        $("#drkdiv").on('click', function(e){
            if( $("#drkquote").css("display")=="block"){
                $("#drkquote").css("display", "none");
            }else{
                $("#drkquote").css("display", " block");
                $("#andyquote").css("display", " none");
                $("#izaquote").css("display", " none");
                $("#susquote").css("display", " none");
                $("#kevquote").css("display", " none");
                $("#helquote").css("display", " none");
                e.stopPropagation();
            }
        });
        $("#heldiv").on('click', function(e){
            if( $("#helquote").css("display")=="block"){
                $("#helquote").css("display", "none");
            }else{
                $("#helquote").css("display", " block");
                $("#izaquote").css("display", " none");
                $("#andyquote").css("display", " none");
                $("#susquote").css("display", " none");
                $("#drkquote").css("display", " none");
                $("#kevquote").css("display", " none");
                e.stopPropagation();
            }
        });

    $(document).click(function(){
        $("#andyquote").css("display", "none");
        $("#izaquote").css("display", "none");
        $("#kevquote").css("display", "none");
        $("#susquote").css("display", " none");
        $("#drkquote").css("display", " none");
        $("#helquote").css("display", " none");
    });

    });
