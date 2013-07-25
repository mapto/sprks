/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/25/13
 * Time: 10:35 AM
 * To change this template use File | Settings | File Templates.
 */
//function for moving characters
    function placeDiv(div_id, l_pos, r_pos, b_pos) {
        var d = document.getElementById(div_id);

        d.style.left = (l_pos)+'%';
        d.style.right = (r_pos)+'%';
        d.style.bottom = (b_pos)+'%';
    }

    function placeAtHome(){

    }

    function placeAtOffice(div_id){
        placeDiv(div_id, 15,80,20);
    }

    function placeAtPublic(){

    }