/**
 * Created with PyCharm.
 * User: Martin
 * Date: 7/30/13
 * Time: 3:07 PM
 * Manages the policy summary frame
 */

//summary of the policy (right corner), called on any policy change
function summarize_policy(policy){
    for (var key in policy){
        if(key==='employee'||key==='location'||key==='device'){
            $("#sum-"+key).text(policy[key]);
        }else if (key==='policyDelta'){
            for (var k in policy[key]){
                var plc = [];
                for (var j in policy[key][k]){
                    if (j==='plen'){
                        if (policy[key][k][j]==='0'){plc.push('policy disabled'); break;}  //let user know that policy is disabled if value of password length is 0
                    }
                    if (j==='pdata'){
                        if (policy[key][k][j]==='0'){plc.push('policy disabled'); break;}  //let user know that policy is disabled if value of bio data is 0
                    }
                    if (j==='bdata'){
                        if (policy[key][k][j]==='0'){plc.push('policy disabled'); break;}  //let user know that policy is disabled if value of pass data is 0
                    }
                    plc.push(j+' '+policy[key][k][j]);
                }
                $("#sum-"+k).text(plc);
                $('.sum-label').each(function(){                            //iterate through policies labels
                    var sumlabel = $(this).attr('class').replace('sum-label', '').replace(' ','').replace('sum-','') ; //biometric/passfaces/pwpolicy
                    if(sumlabel==k){
                        if(!(Object.keys(policy.policyDelta[k]).length===0)){
                           $(this).show();                                              //show policy label if it's not empty'
                        }else{
                           $(this).hide();                                              //hide otherwise
                        }
                    }
                });
            }
        }
        $('.policy-summary').show();
    }
}
