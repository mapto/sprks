plen = document.getElementById("passlen");
psym = document.getElementById("passsym");
pdic = document.getElementById("passdict");
phis = document.getElementById("passhist");
pren = document.getElementById("passrenew");
patt = document.getElementById("passatt");
prec = document.getElementById("passrecovery");

var passAnno = new Anno([
    {
        target: plen,
        content: 'How short do you want passwords to be? Shorter passwords are riskier, but less costly. Generally, employees prefer a password that is neither long or short.',
        position: "top",
        buttons: []
    }
]);

var symAnno = new Anno([
    {
        target: psym,
        content: 'The number of special symbols (i.e. ?,*,/,\,^,& etc) required per password. Less symbols are risky, but less costly. Generally, employees prefer to not have too many symbols.',
        position: "top",
        buttons: []
    }
]);

var dictAnno = new Anno([
    {
        target: pdic,
        content: 'Checking a password against a dictionary means more costs and less risk. Generally, employees do not mind the dictionary check',
        position: "top",
        buttons: []
    }
]);

var histAnno = new Anno([
    {
        target: phis,
        content: 'The cost of checking against a user\'s password history increases the further back to be checked. Generally, employees do not like the history check.',
        position: "top",
        buttons: []
    }
]);

var renewAnno = new Anno([
    {
        target: pren,
        content: 'There\'s high cost to low risk relation the more often a password is renewed. Generally, employees do not like to renew their password often.',
        position: "top",
        buttons: []
    }
]);

var pattAnno = new Anno([
    {
        target: patt,
        content: 'The number of attempts before a system will lock out a user. More attempts are less costly but riskier. Generally, employees will prefer as many attempts as possible.',
        position: "top",
        buttons: []
    }
]);

var recAnno = new Anno([
    {
        target: prec,
        content: 'Are passwords recovered with no human support? Enabling this is costly and less risky. Generally, employees prefer this to contacting tech support.',
        position: "top",
        buttons: []
    }
]);

plen.addEventListener("click", function() {
    passAnno.show();
});

psym.addEventListener("click", function() {
    symAnno.show();
});

pdic.addEventListener("click", function() {
    dictAnno.show();
});

phis.addEventListener("click", function() {
    histAnno.show();
});

pren.addEventListener("click", function() {
    renewAnno.show();
});

patt.addEventListener("click", function() {
    pattAnno.show();
});

prec.addEventListener("click", function() {
    recAnno.show();
});