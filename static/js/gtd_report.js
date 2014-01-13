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
   total: ko.observable()
};

function getReport() {
    $.ajax({
        url: "api/gtd_report",
        type: "GET",
        success: function (report) {
            report = JSON.parse(report);

            for(i=0;i<report['policy'].length;i=i+1){
                reportModel.policy.push(report['policy'][i]);
            }

            for(i=0;i<report['employees'].length;i=i+1){
                reportModel.employees.push({employee: get_full_name(report['employees'][i]['employee']),
                                            risk: report['employees'][i]['risk'].toFixed(2),
                                            p_cost: parseFloat(report['employees'][i]['p_cost'].toFixed(2))});
            }
            reportModel.total({risk:report['total']['risk'],p_cost:report['total']['p_cost']});

            pageModel.currentPage("report_page");

            for (var key in reportModel.policy()[0]){
                $("#policies").append("<div class=\"span1\" id=\"policy_header\"> "+ key +" </div>");
            }
            for (i=0; i<reportModel.policy().length; i=i+1){
                $("#policies").append("<div id=\"policy1\""+i+">")
                for (var key in reportModel.policy()[i]){
                    $("#policies").append(" "+reportModel.policy()[i][key]+" </div>");
                }
                $("#policies").append("</div>");
            }

            for (i=0; i<reportModel.employees().length; i=i+1){
                $("#employees").append("<div id=\"employees\""+i+">"+reportModel.employees()[i]['employee']+"</div>");
                $("#employees_risk").append("<div id=\"employees_risk\""+i+">"+reportModel.employees()[i]['risk']+"</div>");
                $("#employees_cost").append("<div id=\"employees_cost\""+i+">"+reportModel.employees()[i]['p_cost']+"</div>");
            }
            $("#totalrisk").html(reportModel.total()['risk']);
            $("#totalcost").html(reportModel.total()['p_cost']);
        },
        error: function (response) {
            console.log("fail: " + response.responseText);
        }
    });
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