/**
 * Created with PyCharm.
 * User: ZHANELYA
 * Date: 05/09/13
 * Time: 15:50
 * To change this template use File | Settings | File Templates.
 */
/**Called from profile page and policy_summary
 * for generation of reasonable labels
 * and values for the profile table and policy_summary
**/

//function used for profile page
function interpret_policy_label(label){
    switch (label){
        case 'pattempts':
            return 'wrong pswd attempts';
        case 'pdict':
            return 'pswd dictionary check';
        case 'psets':
            return 'symbol sets for pswd';
        case 'bdata':
            return 'biometric';
        case 'phist':
            return 'pswd history check';
        case 'pdata':
            return 'passfaces/ swipe';
        case 'plen':
            return 'pswd length';
        case 'precovery':
            return 'pswd recovery';
        case 'prenew':
            return 'pswd renewal';
        case 'location':
            return 'location';
        case 'device':
            return 'device';
        case 'employee':
            return 'employee';
        default:
            return 'undefined';
    }
}

//function used for profile page and for policy summary
function interpret_policy_value(label,value){
    switch (label){
        case 'pattempts':
            switch (value){
                case '0':
                    return 'unlimited';
                case '1':
                    return '10';
                case '2':
                    return '3';
                default:
                    return 'undefined';
            }
        case 'pdict':
            switch (value){
                case '0':
                    return 'false';
                case '1':
                    return 'true';
                default:
                    return 'undefined';
            }
        case 'psets':
            switch (value){
                case '1':
                    return 'any';
                case '2':
                    return '2';
                case '3':
                    return '3';
                case '4':
                    return '4';
                default:
                    return 'undefined';
            }
        case 'bdata':
            switch (value){
                case '0':
                    return 'none';
                case '1':
                    return 'fingerprint';
                case '2':
                    return 'iris scan';
                default:
                    return 'undefined';
            }
        case 'phist':
            switch (value){
                case '0':
                    return 'none';
                case '1':
                    return 'min';
                case '2':
                    return 'strict';
                case '3':
                    return 'extreme';
                default:
                    return 'undefined';
            }
        case 'pdata':
            switch (value){
                case '0':
                    return 'none';
                case '1':
                    return 'passfaces';
                case '2':
                    return 'swipe';
                default:
                    return 'undefined';
            }
        case 'plen':
            switch (value){
                case '0':
                    return '0';
                case '6':
                    return '6';
                case '8':
                    return '8';
                case '10':
                    return '10';
                case '12':
                    return '12';
                default:
                    return 'undefined';
            }
        case 'precovery':
            switch (value){
                case '0':
                    return '2nd email';
                case '1':
                    return 'secret qn';
                case '2':
                    return 'transaction qn';
                case '3':
                    return 'not applicable';
                default:
                    return 'undefined';
            }
        case 'prenew':
            switch (value){
                case '0':
                    return 'never';
                case '1':
                    return 'annual';
                case '2':
                    return 'quarterly';
                case '3':
                    return 'monthly';
                default:
                    return 'undefined';
            }
        default:
            return 'undefined';
    }
}