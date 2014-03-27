/**
 * Created with PyCharm.
 * User: ZHANELYA
 * Date: 12/01/14
 * Time: 23:20
 * To change this template use File | Settings | File Templates.
 */
reportModel = {
   policy: ko.observableArray(),
   employees: ko.observableArray(),
   total: ko.observable(),
   e_risks: ko.observableArray(),
   e_costs: ko.observableArray(),
   employees_number:ko.observable()
};
$(function(){
    reportModel.employees_number.subscribe(function (employees_number) {
        getReport(employees_number);
    });
});

//To dynemically change the number of employees, call:
// reportModel.employees_number(1)

function clearReport(){
    reportModel.policy([]);
    reportModel.total('');
    reportModel.employees([]);
    $('#report_error').children().remove();
    $("#policies").children().remove();
    $("#employees").children().remove();
    $("#employees_risk").children().remove();
    $("#employees_cost").children().remove();
    $("#total_container").children().remove();;
    $("#total_risk_container").children().remove();;
    $("#total_cost_container").children().remove();;

}

function get_m_ranges(modifier, vals){
    var max = Math.max.apply(Math, vals);
    if(modifier ==0){
        return 10;
    }else if(modifier<=0.2*max){
        return 2;
    }else if(modifier<=0.4*max){
        return 4;
    }else if(modifier<=0.6*max){
        return 6;
    }else if(modifier<=0.8*max){
        return 8;
    }else{
        return 10;
    }
}

function get_m_ranges_total(modifier, vals){
    if(modifier ==0){
        return 0;
    }else if(modifier<=0.1){
        return 1;
    }else if(modifier<=0.2){
        return 2;
    }else if(modifier<=0.3){
        return 3;
    }else if(modifier<=0.4){
        return 4;
    }else if(modifier<=0.5){
        return 5;
    }else if(modifier<=0.6){
        return 6;
    }else if(modifier<=0.7){
        return 7;
    }else if(modifier<=0.8){
        return 8;
    }else if(modifier<=0.9){
        return 9;
    }else if(modifier<=1){
        return 10;
    }else{
        return 10;
    }
}

function get_full_name(abbreviation){
    switch (abbreviation){
        case 'padh':
            return 'PA to Department Head';
        case 'som':
            return 'Senior Operations Manager';
        case 'bdd':
            return 'Business Development Director';
        case 'cam':
            return 'Client Account Manager';
        case 'rm':
            return 'Recruitment Manager';
        case 'pm':
            return 'Project Manager';
        case 'ft':
            return 'Facilities Technician';
        case 'sc':
            return 'Sales Consultant';
        case 'sm':
            return 'Suppliers Manager';
        default:
            return 'unknown';

    }
}

function get_employee_type(position){
    switch (position){
        case 'padh':
            return 'executive';
        case 'som':
            return 'executive';
        case 'bdd':
            return 'executive';
        case 'cam':
            return 'desk';
        case 'rm':
            return 'desk';
        case 'pm':
            return 'desk';
        case 'ft':
            return 'road';
        case 'sc':
            return 'road';
        case 'sm':
            return 'road';
        default:
            return 'other';

    }
}

function getReport(employees_number) {
    if(employees_number){
        $.ajax({
            url: "api/gtd_report",
            type: "POST",
            data: JSON.stringify({employees_number:employees_number}),
            success: function (report) {
                clearReport();
                report = JSON.parse(report);
                for(i=0;i<report['employees'].length;i=i+1){
                    var employee_type = get_employee_type(report['employees'][i]['employee']);
                    reportModel.employees.push({employee: '<span class="'+employee_type+'">'+get_full_name(report['employees'][i]['employee'])+'('+employee_type+'</span>)',
                                                risk: report['employees'][i]['risk'].toFixed(2),
                                                p_cost: parseFloat(report['employees'][i]['p_cost'].toFixed(2))});
                    reportModel.e_risks.push(-report['employees'][i]['risk'].toFixed(2))
                    reportModel.e_costs.push(parseFloat(report['employees'][i]['p_cost'].toFixed(2)))
                }
                reportModel.total({risk:1+report['total']['risk'],p_cost:0+report['total']['p_cost']}); //Initial risk is very high(1 or 100%) whereas productivity is 0
                //policy report
                for(i=0;i<report['policy'].length;i=i+1){
                    reportModel.policy.push(report['policy'][i]);
                }
                //create table dynamically:
                var table = $('<table></table>').addClass('profile_table');
                //provide column names:
                var row = $('<tr></tr>').addClass('profileTr');
                row.append($('<td><image style="width:45%" title="employee" src="static/img/policy_icons/employee.png"></image></td>').addClass('profileTd profileTh'));
                row.append($('<td><image style="width:45%" title="location" src="static/img/policy_icons/location.png"></image></td>').addClass('profileTd profileTh'));
                row.append($('<td><image style="width:45%" title="device" src="static/img/policy_icons/device.png"></image></td>').addClass('profileTd profileTh'));
                for (var key in reportModel.policy()[0]) {
                    if (key !== 'location' && key !== 'device' && key !== 'employee' && key !== 'bdata' && key !== 'pdata') { //do not show these fields
                        var col = $('<td><image style="width:45%" title="'+interpret_policy_label(key)+'" src="static/img/policy_icons/'+key+'.png"></image></td>').addClass('profileTd profileTh');
                        row.append(col);
                    }
                }
                table.append(row);
                //fill table:
                var row = [];
                var col = [];
                var location_r = [];
                var device_r = [];
                var employee_r = [];
                var tmp;
                for (var i in reportModel.policy()) {
                    var obj = reportModel.policy()[i];
                    col[i] = {};
                    row [i] = $('<tr></tr>').addClass('profileTr' + i);
                    var location_img = "static/img/"+obj['location']+".png";
                    location_r[i] = $('<td><image style="width:45%" title="'+obj['location']+'" src="'+location_img+'"></image></td>').addClass('profileTd location'+i);
                    var device_img = "static/img/"+obj['device']+".png";
                    device_r[i] = $('<td><image style="width:45%" title="'+obj['device']+'" src="'+device_img+'"></image></td>').addClass('profileTd device'+i);
                    var employee_img = "static/img/"+obj['employee']+".png";
                    employee_r[i] = $('<td><image style="width:45%" title="'+obj['employee']+'" src="'+employee_img+'"></image></td>').addClass('profileTd employee'+i);
                    row[i].append(employee_r[i]);
                    row[i].append(location_r[i]);
                    row[i].append(device_r[i]);
                    for (var k in obj) {
                        var attrName = k; //e.g. pdict
                        var attrValue = obj[k]; //e.g. 1
                        if (attrName !== 'location' && attrName !== 'device' && attrName !== 'employee' && attrName !== 'bdata' && attrName !== 'pdata') { //do not show these fields
                            if(attrName=='pdict'){
                                if(attrValue==1){
                                    col[i][attrName] = $('<td><image style="width:45%" title="set" src="static/img/policy_icons/check.png"></image></td>').addClass('profileTd ' + attrName + i);
                                }else if(attrValue==0){
                                    col[i][attrName] = $('<td><image style="width:45%" title="none" src="static/img/policy_icons/cross.png"></image></td>').addClass('profileTd ' + attrName + i);
                                }
                            }else{
                                col[i][attrName] = $('<td></td>').addClass('profileTd ' + attrName + i).text(interpret_policy_value(attrName,attrValue));
                            }
                            row [i].append(col[i][attrName]);
                        }
                    }
                    if (row[i].text() != '') { //check if the row contains anything
                        table.append(row[i]);
                    }
                }
                $('#policies').append(table);
                var scale = "<div class='scale_container'>"+
                                "<div class='scale_label'>0</div>" +
                                "<div class='scale_label'>Low</div>" +
                                "<div class='scale_label'>Medium</div>" +
                                "<div class='scale_label'>High</div>" +
                                "<div class='scale_label'>Extreme</div>" +
                                "<div class='scale'>|</div>" +
                                "<div class='scale'>|</div>" +
                                "<div class='scale'>|</div>" +
                                "<div class='scale'>|</div>" +
                                "<div class='scale'>|</div>" +
                            "</div><br/>";
                var scale_total = "<div class='scale_container'>"+
                                "<div class='scale_label total'>0</div>" +
                                "<div class='scale_label total'>20</div>" +
                                "<div class='scale_label total'>40</div>" +
                                "<div class='scale_label total'>60</div>" +
                                "<div class='scale_label total'>80</div>" +
                                "<div class='scale_label total'>100</div>" +
                                "<div class='scale total'>|</div>" +
                                "<div class='scale total'>|</div>" +
                                "<div class='scale total'>|</div>" +
                                "<div class='scale total'>|</div>" +
                                "<div class='scale total'>|</div>" +
                                "<div class='scale total'>|</div>" +
                            "</div><div>(%)</div><br/>";
                $("#employees").append("<div class='scale_container' style='margin-top:12%;'></div>");
                $("#employees_risk").append(scale);
                $("#employees_cost").append(scale);
                for (i=0; i<reportModel.employees().length; i=i+1){
                    $("#employees").append("<div id=\"employees"+i+"\">"+reportModel.employees()[i]['employee']+"</div>");
                    //$("#employees_risk").append("<div id=\"employees_risk"+i+"\">"+reportModel.employees()[i]['risk']+"</div>");
                    $("#employees_risk").append("<div id=\"employees_risk"+i+"\"></div>");
                    $("#employees_risk"+i).addClass("modifiers_range m_risk mr_"+get_m_ranges(-reportModel.employees()[i]['risk'], reportModel.e_risks()));
                    //risk value is negated to make it positive for calculation of ranges image, the value remains negative
                    //$("#employees_cost").append("<div id=\"employees_cost"+i+"\">"+reportModel.employees()[i]['p_cost']+"</div>");
                    $("#employees_cost").append("<div id=\"employees_cost"+i+"\"></div>");
                    $("#employees_cost"+i).addClass("modifiers_range m_cost mr_"+get_m_ranges(reportModel.employees()[i]['p_cost'], reportModel.e_costs()));
                }
                $("#total_container").append("<div class='scale_container' style='margin-top:12%;'></div>");
                $("#total_risk_container").append(scale_total+"<div id='totalrisk'></div>");
                $("#total_cost_container").append(scale_total+"<div id='totalcost'></div>");

                //$("#totalrisk").html(reportModel.total()['risk'].toFixed(2));
                //$("#totalcost").html(reportModel.total()['p_cost'].toFixed(2));
                $("#totalrisk").addClass("modifiers_total m_risk mr_"+get_m_ranges_total(reportModel.total()['risk']));
                $("#totalcost").addClass("modifiers_total m_cost mr_"+get_m_ranges_total(reportModel.total()['p_cost']));
            },
            error: function (response) {
                clearReport();
                console.log("fail: " + response.responseText);
                $('#report_error').append("<div>No report available</div>");
            }
        });
    }else{
        clearReport();
        $('#report_error').append("<div>No report available</div>");
    }
}