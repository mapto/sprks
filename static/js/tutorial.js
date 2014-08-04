var tick = document.getElementById("myswitch"); // store toggle switch to tick variable
var curStep;
var cookieName = "tutorials";

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
checkCookie();

function checkCookie() {
    var cookie = getCookie();
    if (cookie === "on") {
        tick.checked = true;
    } else {
        tick.checked = false;
    }
}

function getCookie() {
    var name = cookieName + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "";
}

function setCookie(value) {
    document.cookie = cookieName + "=" + value + ";";
    console.log(document.cookie);
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
        cookie = setCookie("on");
        console.log(cookie);
    } else {
        console.log('else cookie');
        tick.checked = false;
        cookie = setCookie("off");
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
        }
    } else {
        introJs().exit();
        setCookie("off");
    }
}

window.onload = setTimeout(function() { autoStart();console.log('on load ' + getCookie()); }, 2000);

/*
    Intro / Jan tutorials
*/
function startTutorial() {
    setCookie("on");
    tut = introJs()
    tut.onexit(function(){
        curStep = tut.nextStep()._currentStep;
        tut.exit(); // needed since last step will move the presentation forward, messing the CSS
        tick.checked = false;
    });
    tut.oncomplete(function() { console.log('intro finished'); });
    tut.setOptions({
        exitOnOverlayClick: true,
        scrollToElement: false,
        showStepNumbers: false,
        steps: [
            {
                intro: "Welcome to UCL's Information Security Simulation, SPRKS"
            },
            {
                intro: "This is a turn-based game where you are in charge of Information Security Policies for energy company Global Sparks over the course of a thirteen months."
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
                element: "#timeline",
                intro: "Your monthly progress is displayed in the timeline",
                position: "right"
            },
            {
                element: "#interview1",
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
    tut.start();
}

function passTutorial() {
    setCookie("on");
    pass = introJs();
    pass.setOptions({
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
    pass.start();
}
tick.addEventListener("click", autoStart);