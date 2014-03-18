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
   employees_number:ko.observable(1)
};
$(function(){
    reportModel.employees_number.subscribe(function (employees_number) {
        getReport(employees_number);
    });
});

//To dynemically change the number of employees, call:
// reportModel.employees_number(1)

function getReport(employees_number) {
    if(employees_number){
        clearReport();
        $.ajax({
            url: "api/gtd_report",
            type: "POST",
            data: JSON.stringify({employees_number:employees_number}),
            success: function (report) {
                report = JSON.parse(report);
                for(i=0;i<report['employees'].length;i=i+1){
                    reportModel.employees.push({employee: get_full_name(report['employees'][i]['employee'])+' ('+get_employee_type(report['employees'][i]['employee'])+')',
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
                row.append($('<td></td>').addClass('profileTd profileTh').text("employee"));
                row.append($('<td></td>').addClass('profileTd profileTh').text("device"));
                row.append($('<td></td>').addClass('profileTd profileTh').text("location"));
                for (var key in reportModel.policy()[0]) {
                    if (key !== 'location' && key !== 'device' && key !== 'employee') { //do not show these fields
                        var col = $('<td></td>').addClass('profileTd profileTh').text(interpret_policy_label(key));
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
                    location_r[i] = $('<td></td>').addClass('profileTd location'+i).text(obj['location']);
                    device_r[i] = $('<td></td>').addClass('profileTd device'+i).text(obj['device']);
                    employee_r[i] = $('<td></td>').addClass('profileTd employee'+i).text(obj['employee']);
                    row[i].append(employee_r[i]);
                    row[i].append(device_r[i]);
                    row[i].append(location_r[i]);
                    for (var k in obj) {
                        var attrName = k; //e.g. pdict
                        var attrValue = obj[k]; //e.g. 1

                        if (attrName !== 'location' && attrName !== 'device' && attrName !== 'employee') { //do not show these fields
                            col[i][attrName] = $('<td></td>').addClass('profileTd ' + attrName + i).text(interpret_policy_value(attrName,attrValue));
                            row [i].append(col[i][attrName]);
                        }
                    }
                    if (row[i].text() != '') { //check if the row contains anything
                        table.append(row[i]);
                    }
                }
                $('#policies').append(table);

                for (i=0; i<reportModel.employees().length; i=i+1){
                    $("#employees").append("<div id=\"employees"+i+"\">"+reportModel.employees()[i]['employee']+"</div>");
                    $("#employees_risk").append("<div id=\"employees_risk"+i+"\">"+reportModel.employees()[i]['risk']+"</div>");
                    $("#employees_risk"+i).addClass("modifiers_range m_risk mr_"+get_m_ranges(reportModel.employees()[i]['risk'], reportModel.e_risks()));
                    //risk value is negated to make it positive for calculation of ranges image, the value remains negative
                    $("#employees_cost").append("<div id=\"employees_cost"+i+"\">"+reportModel.employees()[i]['p_cost']+"</div>");
                    $("#employees_cost"+i).addClass("modifiers_range m_cost mr_"+get_m_ranges(reportModel.employees()[i]['p_cost'], reportModel.e_costs()));
                }
                $("#totalrisk").html(reportModel.total()['risk'].toFixed(2));
                $("#totalcost").html(reportModel.total()['p_cost'].toFixed(2));
                $("#totalrisk").addClass("modifiers_total m_risk mr_"+get_m_ranges_total(reportModel.total()['risk']));
                $("#totalcost").addClass("modifiers_total m_cost mr_"+get_m_ranges_total(reportModel.total()['p_cost']));
            },
            error: function (response) {
                console.log("fail: " + response.responseText);
                $('#policies').append("<div>No report available</div>");
            }
        });
    }
}

function clearReport(){
    reportModel.policy([]);
    reportModel.total('');
    reportModel.employees([]);
    $("#policies").children().remove();
    $("#employees").children().remove();
    $("#employees_risk").children().remove();
    $("#employees_cost").children().remove();
}

function get_m_ranges(modifier, vals){ //TODO adjust values for modifier
    if(modifier ==0){
        return 0;
    }else if(modifier<=0.02){
        return 2;
    }else if(modifier<=0.04){
        return 4;
    }else if(modifier<=0.06){
        return 6;
    }else if(modifier<=0.08){
        return 8;
    }else if(modifier<=0.10){
        return 10;
    }else{
        return 10;
    }
}

function get_m_ranges_total(modifier, vals){ //TODO adjust values for modifier
    if(modifier ==0){
        return 0;
    }else if(modifier<=0.2){
        return 2;
    }else if(modifier<=0.4){
        return 4;
    }else if(modifier<=0.6){
        return 6;
    }else if(modifier<=0.8){
        return 8;
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