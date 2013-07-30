/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/26/13
 * Time: 2:24 PM
 * To change this template use File | Settings | File Templates.
 */
function cast_month(month){
    var months = {
        'January' : '1',
        'February' : '2',
        'March' : '3',
        'April' : '4',
        'May' : '5',
        'June' : '6',
        'July' : '7',
        'August' : '8',
        'September' : '9',
        'October' : '10',
        'November' : '11',
        'December' : '12'
    };

    for (var month_string in months){
        var month_num = months[month_string]
        if(month_string===month){
            return month_num
        }else if(month_num===month){
            return month_string
        }
    }
}

function time_visualiser(date, show_year){
    //converts from "YYYY-MM-DD" to "D Month YYYY"
    if (date != "") {
            var d1 = new Date(date);
            if (d1 == null) {
                console.log('Date Invalid.');
            }else{
                var year = show_year ? d1.getFullYear().toString() : "";
                var date_array = d1.getDate().toString()+ ' '+ cast_month((d1.getMonth()+1).toString())+' ' + year;
                var string_date = date_array;
            }
    }
    return string_date;
}
function time_parser(string_date){
    //converts from "D Month YYYY" to "YYYY-MM-DD"
    if (string_date != "") {
            var date_array =string_date.split(" ");
            var date = date_array[2] +'-'+ cast_month(date_array[1]) +'-'+ date_array[0];
    }
    return date;
}