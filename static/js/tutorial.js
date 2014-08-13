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
    setCookie(cookieName, "on");
    tut = introJs()
    switch (turn) {
        case "0" :
            first.style.background = risky;
            second.style.background = costly;
            third.style.background = blue;
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
            break;
        case "1":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Nice work getting through your first month"
                    },
                    {
                        element: "#izadiv",
                        intro: "Make sure to talk to your employees after every month",
                        position: "left"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "2":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Having a different set of policies for those that work from home is a difficult choice for ISOs. One that in this simulation, you won't have to make"
                    },
                    {
                        intro: "But if we had implemented a work-from-home scenario, you would need to reconsider the settings for all your policies"
                    },
                    {
                        intro: "After all, working from home opens a few more vulnerabilities in any system"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "3":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        element: "#andydiv",
                        intro: "Seems like you've got one more person to oversee",
                        position: "left"
                    },
                    {
                        intro: "Since Andrew and Iza are &quot;desk workers&quot; their password policies should be similar"
                    },
                    {
                        intro: "As numbers keep growing, you should keep in mind that what works for one may not for the other"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "4":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Until now, your division has only used desktop terminals",
                    },
                    {
                        intro: "And laptops are particularly susceptible to attacks"
                    },
                    {
                        intro: "You'll have to consider that going into this month's policies"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "5":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Quiet indeed",
                    },
                    {
                        element: "#izadiv",
                        intro: "Andrew and Iza will still help, though"
                    },
                    {
                        intro: "Just go about this month as you normally would"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "6":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "So much for a little quiet...",
                    },
                    {
                        intro: "The cross-division training won't affect you too much"
                    },
                    {
                        element: "#employees",
                        intro: "The &quot;Away&quot; policies for all your employees will be handled by Kevin and Susie's division",
                        position: "left"
                    },
                    {
                        intro: "Of course, that could mean that you may just have to handle someone else's policies in the future"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "7":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        element: "#heldiv",
                        intro: "An executive worker's policies have to be a bit more relaxed",
                        position: "left"
                    },
                    {
                        element: "#drkdiv",
                        intro: "Higher security clearance, if you will",
                        position: "left"
                    },
                    {
                        intro: "At the same time, their information needs to be better secured"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "8":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Obviously passwords are not the only way to keep information secure",
                    },
                    {
                        intro: "A company will consider many factors before acquiring a new technology architecture"
                    }
                    {
                        intro: "Installation and training costs as well as return on investment are only a couple of such factors"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "9":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Passface security uses pictures instead of alphanumerical characters as a base to create a passcode",
                    },
                    {
                        intro: "Outsourcing works best while Global Sparks stabilizes itself"
                    },
                    {
                        intro: "You should start thinking about how you would handle image-based passwords' policies "
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "10":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "Biometrics will often involve fingerprint identification",
                    },
                    {
                        intro: "Retina scanning is also a possibility, as is voice recognition"
                    },
                    {
                        intro: "How would you handle such security?"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "11":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "There is a major difference between passwords/passfaces and biometrics"
                    },
                    {
                        intro: "With biometrics, you must also consider the upkeep of hardware (scanners, readers and/or microphones)"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case "12":
            tut.setOptions({
                exitOnOverlayClick: false,
                scrollToElement: false,
                showStepNumbers: false,
                steps: [
                    {
                        intro: "As you have hopefully gathered by now, ISOs strive for balance",
                    },
                    {
                        intro: "The risks and costs will more than likely never please everyone"
                    },
                    {
                        intro: "Their work is a challenging one and crucial to a company's future"
                    },
                    {
                        intro: "So if you're wondering why your password policies are the way they are"
                    },
                    {
                        intro: "You can rest easy knowing that it is all for your and your company's own good"
                    }
                ]
            });
            tut.onexit(function(){
                curStep = tut.currentStep();
                tick.checked = false;
                setCookie(cookieName, "off");
            });
            break;
        case default:
            break;
    }
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