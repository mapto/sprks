var tick = document.getElementById("myswitch"); // store toggle switch to tick variable
var iupper = document.getElementById("impress-upper"); // store upper impress div in iupper variable
var ilower = document.getElementById("impress-lower"); // store lower impress div in ilower variable
var curStep = 1; // by default all introductions start at the beginning
var costly = "#369ead";
var risky = "#c24642";
var blue = "blue";
var gray = "gray";
var cookieName = "tutorials";
var cookieImpressU = "iupper";
var cookieImpressL = "ilower";

/*
    pointTutorial highlights the tutorials switch at a certain interval and hides it shortly after.

function pointTutorial(flag) {
    var intro = introJs();
    intro.setOptions({
        showBullets: false,
        exitOnEsc: true,
        exitOnOverlayClick: true,
        scrollToElement: false,
        showStepNumbers: false,
        showButtons: false,
        steps:[
            {
                element: '#tutdiv',
                intro: "Click me if you'd like some help",
                position: 'right'
            }
            ]
    });
    if (flag === 1) {
        intro.start();
        tick.disabled = true;
    }
    if (flag === 2) {
        tick.disabled = false;
        intro.exit();
    }
}

setTimeout(function() { pointTutorial(1) }, 40000);
setTimeout(function() { pointTutorial(2) }, 45000);
*/

/*
    cookie helper functions (checker, getter and setter)
*/

function checkCookie(name) {
    var cookie = getCookie(name);
    console.log(cookie);
    if (cookie === "on") {
        tick.checked = true;
    } else {
        tick.checked = false;
    }
}

function getCookie(name) {
    var cookieN = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring((name.length + 1), c.length); // the +1 removes "=" from return val
    }
    return "";
}

function setCookie(name, value) {
    document.cookie = name + "=" + value + ";";
    console.log(document.cookie);
}

if (document.title === "Incident") {
    setCookie(cookieImpressU, iupper.innerHTML);
    setCookie(cookieImpressL, ilower.innerHTML);
}
if (document.title === "Impress" ) {
    document.getElementById("upincident").innerHTML = getCookie(cookieImpressU);
    document.getElementById("loincident").innerHTML = getCookie(cookieImpressL);
}
/*
    check cookie for tutorial switch position
*/
checkTutorial();

function checkTutorial() {
    cookie = getCookie(cookieName);
    if (cookie === "on") {
        console.log('if cookie');
        tick.checked = true;
        cookie = setCookie(cookieName, "on");
        console.log(cookie);
    } else {
        console.log('else cookie');
        tick.checked = false;
        cookie = setCookie(cookieName, "off");
        console.log(cookie);
    }
}

/*
    on load, start tutorials after a short time (2s) if switch in on

*/

function autoStart() {
    console.log('tick: before autostart');
    if (tick.checked) {
        switch (title) {
            case "Introduction":
                startTutorial();
                break;
            case "Password policy":
                passTutorial();
                break;
            case "Incident":
                inciTutorial();
                break;
        }
    } else {
        introJs().exit();
        setCookie(cookieName, "off");
    }
}

window.onload = setTimeout(function() { autoStart();console.log('on load ' + getCookie()); }, 2000);

/*
    Intro / Jan tutorials
*/
function startTutorial() {
    first.style.background = risky;
    second.style.background = costly;
    third.style.background = blue;
    setCookie(cookieName, "on");
    tut = introJs()
    tut.setOptions({
        exitOnOverlayClick: false,
        scrollToElement: false,
        showStepNumbers: false,
        steps: [
            {
                intro: "Welcome to UCL's Information Security Simulation, SPRKS"
            },
            {
                intro: "This is a turn-based game where you are in charge of Information Security Policies for energy company Global Sparks over the course of thirteen months."
            },
            {
                intro: "Each turn the game should process as such:"
            },
            {
                element: "#maindiv",
                intro: "All relevant content will be displayed here",
                position: "right"
            },
            {
                element: "#story",
                intro: "You can check your story at the start of every turn",
                position: "right"
            },
            {
                element: "#policy",
                intro: "Change policies as needed",
                position: "right"
            },
            {
                element: "#conseq",
                intro: "Check the results for the chosen policies",
                position: "right"
            },
            {
                element: "#score",
                intro: "end the turn???", //TODO: figure out what it's actually supposed to do...
                position: "right"
            },
            {
                element: "#timesec",
                intro: "The timeline will keep track of your policies' results",
                position: "bottom"
            },
            {
                element: "#first",
                intro: "If your policy was too risky",
                position: "bottom"
            },
            {
                element: "#second",
                intro: "Too costly",
                position: "bottom"
            },
            {
                element: "#third",
                intro: "Or balanced"
            },
            {
                element: "#izadiv",
                intro: "If you're stuck, you can always talk to your employees for some hints",
                position: "left"
            },
            {
                intro: "Aim to set the best policies for the company during your stay"
            },
            {
                intro: "Good Luck!"
            }
        ]
    });
    tut.onexit(function(){
        second.style.background = third.style.background = first.style.background = gray;
        console.log(tut._currentStep + ' on exit before ' + curStep);
        curStep = tut.currentStep();
        console.log(tut._currentStep + ' on exit after ' + curStep);
        tick.checked = false;
        setCookie(cookieName, "off");
    });
    tut.oncomplete(function() {
        second.style.background = third.style.background = first.style.background = gray;
        console.log('intro finished');
    });
    console.log(curStep + 'inside tut');
    tut.goToStep(curStep).start();
}

/*
    Policies tutorial
*/
function passTutorial() {
    setCookie(cookieName, "on");
    pass = introJs();
    pass.setOptions({
        exitOnOverlayClick: false,
        showStepNumbers: false,
        scrollToElement: true,
        steps: [
            {
                intro: "On this page you can set policies for your employee"
            },
            {
                element: "#maindiv",
                intro: "For now it's best to go with a trial and error strategy",
                position: "right"
            },
            {
                element: "#plen",
                intro: "Changing a policy will display a chart of risk compared to cost"
            },
            {
                element: "#passlen",
                intro: "If you'd like to know more about each item, the tooltips will help you"
            },
            {
                intro: "You can click anywhere outside a tooltip to close it"
            }
        ]
    });
    pass.onexit(function(){
        console.log(pass._currentStep + ' on exit before ' + curStep);
        curStep = pass.currentStep();
        console.log(pass._currentStep + ' on exit after ' + curStep);
        tick.checked = false;
        setCookie(cookieName, "off");
    });
    pass.oncomplete(function() { console.log('pass finished'); });
    console.log(curStep + 'inside tut');
    pass.goToStep(curStep).start();
}

/*
    Incident tutorial
*/
function inciTutorial() {
    setCookie(cookieName, "on");
    inci = introJs();
    inci.setOptions({
        exitOnOverlayClick: false,
        showStepNumbers: false,
        scrollToElement: true,
        steps: [
            {
                intro: "This page will show the results from you policy settings"
            },
            {
                element: "#description",
                intro: "The biggest factor of your policy will be shown",
                position: "right"
            },
            {
                element: "#event",
                intro: "An event that stemmed from the policy"
            },
            {
                element: "#consequences",
                intro: "What that event meant for your division"
            },
            {
                element: "#type",
                intro: "The biggest risk type your policy has"
            },
            {
                element: "#risk",
                intro: "And the possibility of that risk happening."
            }
        ]
    });
    inci.onexit(function(){
        console.log(inci._currentStep + ' on exit before ' + curStep);
        curStep = inci.currentStep();
        console.log(inci._currentStep + ' on exit after ' + curStep);
        tick.checked = false;
        setCookie(cookieName, "off");
    });
    inci.oncomplete(function() { console.log('incident finished'); });
    console.log(curStep + 'inside tut');
    inci.goToStep(curStep).start();
}

tick.addEventListener("click", autoStart);