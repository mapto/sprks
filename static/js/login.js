/*wait until document is loaded*/

jQuery(document).ready(function() {
        jQuery("#login_drop").on('click', function(){
           if( jQuery("#login").css("display")=="none"){
               jQuery("#login").css("display", "block");
           }else{
                jQuery("#login").css("display", "none");
           }

        });

});

