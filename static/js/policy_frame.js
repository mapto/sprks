/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/30/13
 * Time: 3:07 PM
 * To change this template use File | Settings | File Templates.
 */
function summarize_policy(policy){ //summary of the policy (right corner), called on any policy change
    for (var key in policy){
        if(key==='employee'||key==='location'||key==='device'){
            $("#sum-"+key).text(policy[key]);
        }else if (key==='policyDelta'){
            for (var k in policy[key]){
                var plc = [];
                for (var j in policy[key][k]){
                    if (j==='plen'){
                        if (policy[key][k][j]==='0'){plc = []; break;} //null password policy in summary if plen is set to '0'
                    }
                    plc.push(j+' '+policy[key][k][j]);
                }
                $("#sum-"+k).text(plc);
            }
        }
        $('.policy-summary').show();
    }
}
