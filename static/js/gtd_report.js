/**
 * Created with PyCharm.
 * User: ZHANELYA
 * Date: 12/01/14
 * Time: 23:20
 * To change this template use File | Settings | File Templates.
 */
reportModel = {
   policy: ko.observable(),
   employees: ko.observable()
};

function getReport() {
    $.ajax({
        url: "api/gtd_report",
        type: "GET",
        success: function (report) {
            console.log(report);
            reportModel.policy("policy");
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