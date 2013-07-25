/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/25/13
 * Time: 10:35 AM
 * To change this template use File | Settings | File Templates.
 */
//function for moving characters (class interviewee, ids:interview1,interview2,interview3)

    var coordinates = {};
    coordinates.interview1 = {};
    coordinates.interview2 = {};
    coordinates.interview3 = {};

    coordinates.interview1.home = [40, 55, 55];
    coordinates.interview1.public = [55, 40, 20];
    coordinates.interview1.office = [15, 80, 20];

    coordinates.interview2.home = [47.5, 47.5, 55];
    coordinates.interview2.public = [62.5, 32.5, 20];
    coordinates.interview2.office = [22.5, 72.5, 20];

    coordinates.interview3.home = [55, 40, 55];
    coordinates.interview3.public = [70, 25, 20];
    coordinates.interview3.office = [30, 65, 20];


    function placeDiv(div_id, l_pos, r_pos, b_pos) {
        var d = document.getElementById(div_id);
        d.style.left = (l_pos)+'%';
        d.style.right = (r_pos)+'%';
        d.style.bottom = (b_pos)+'%';
    }

    function place_at(div_id, place){
        var l = coordinates[div_id][place][0];
        var r = coordinates[div_id][place][1];
        var b = coordinates[div_id][place][2];
        placeDiv(div_id, l,r,b);                                        //update charachter position
        placeDiv('quote'+div_id.substr(div_id.length-1),l-12.5,r+12.5,b+18);  //update position of his speech bubble
    }

    function UpdateCharacters(data){ //data: interview1 - location, device; interview2 - loc, dev; interview3 - loc, dev
        place_at('interview2', 'office');
        place_at('interview1', 'office');
        place_at('interview3', 'office');

    }