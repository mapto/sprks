// MooTools: the javascript framework.
// Load this file's selection again by visiting: http://mootools.net/more/cbf2909f532bfaecd87d1f6d8da99cb8 
// Or build this file again with packager using: packager build More/Fx.Accordion
/*
 ---

 script: More.js

 name: More

 description: MooTools More

 license: MIT-style license

 authors:
 - Guillermo Rauch
 - Thomas Aylott
 - Scott Kyle
 - Arian Stolwijk
 - Tim Wienk
 - Christoph Pojer
 - Aaron Newton
 - Jacob Thornton

 requires:
 - Core/MooTools

 provides: [MooTools.More]

 ...
 */

MooTools.More = {
    'version': '1.4.0.1',
    'build': 'a4244edf2aa97ac8a196fc96082dd35af1abab87'
};


/*
 ---

 script: Fx.Elements.js

 name: Fx.Elements

 description: Effect to change any number of CSS properties of any number of Elements.

 license: MIT-style license

 authors:
 - Valerio Proietti

 requires:
 - Core/Fx.CSS
 - /MooTools.More

 provides: [Fx.Elements]

 ...
 */

Fx.Elements = new Class({

    Extends: Fx.CSS,

    initialize: function (elements, options) {
        this.elements = this.subject = $$(elements);
        this.parent(options);
    },

    compute: function (from, to, delta) {
        var now = {};

        for (var i in from) {
            var iFrom = from[i], iTo = to[i], iNow = now[i] = {};
            for (var p in iFrom) iNow[p] = this.parent(iFrom[p], iTo[p], delta);
        }

        return now;
    },

    set: function (now) {
        for (var i in now) {
            if (!this.elements[i]) continue;

            var iNow = now[i];
            for (var p in iNow) this.render(this.elements[i], p, iNow[p], this.options.unit);
        }

        return this;
    },

    start: function (obj) {
        if (!this.check(obj)) return this;
        var from = {}, to = {};

        for (var i in obj) {
            if (!this.elements[i]) continue;

            var iProps = obj[i], iFrom = from[i] = {}, iTo = to[i] = {};

            for (var p in iProps) {
                var parsed = this.prepare(this.elements[i], p, iProps[p]);
                iFrom[p] = parsed.from;
                iTo[p] = parsed.to;
            }
        }

        return this.parent(from, to);
    }

});


/*
 ---

 script: Fx.Accordion.js

 name: Fx.Accordion

 description: An Fx.Elements extension which allows you to easily create accordion type controls.

 license: MIT-style license

 authors:
 - Valerio Proietti

 requires:
 - Core/Element.Event
 - /Fx.Elements

 provides: [Fx.Accordion]

 ...
 */

Fx.Accordion = new Class({

    Extends: Fx.Elements,

    options: {/*
     onActive: function(toggler, section){},
     onBackground: function(toggler, section){},*/
        fixedHeight: false,
        fixedWidth: false,
        display: 0,
        show: false,
        height: true,
        width: false,
        opacity: true,
        alwaysHide: false,
        trigger: 'click',
        initialDisplayFx: true,
        resetHeight: true
    },

    initialize: function () {
        var defined = function (obj) {
            return obj != null;
        };

        var params = Array.link(arguments, {
            'container': Type.isElement, //deprecated
            'options': Type.isObject,
            'togglers': defined,
            'elements': defined
        });
        this.parent(params.elements, params.options);

        var options = this.options,
            togglers = this.togglers = $$(params.togglers);

        this.previous = -1;
        this.internalChain = new Chain();

        if (options.alwaysHide) this.options.link = 'chain';

        if (options.show || this.options.show === 0) {
            options.display = false;
            this.previous = options.show;
        }

        if (options.start) {
            options.display = false;
            options.show = false;
        }

        var effects = this.effects = {};

        if (options.opacity) effects.opacity = 'fullOpacity';
        if (options.width) effects.width = options.fixedWidth ? 'fullWidth' : 'offsetWidth';
        if (options.height) effects.height = options.fixedHeight ? 'fullHeight' : 'scrollHeight';

        for (var i = 0, l = togglers.length; i < l; i++) this.addSection(togglers[i], this.elements[i]);

        this.elements.each(function (el, i) {
            if (options.show === i) {
                this.fireEvent('active', [togglers[i], el]);
            } else {
                for (var fx in effects) el.setStyle(fx, 0);
            }
        }, this);

        if (options.display || options.display === 0 || options.initialDisplayFx === false) {
            this.display(options.display, options.initialDisplayFx);
        }

        if (options.fixedHeight !== false) options.resetHeight = false;
        this.addEvent('complete', this.internalChain.callChain.bind(this.internalChain));
    },

    addSection: function (toggler, element) {
        toggler = document.id(toggler);
        element = document.id(element);
        this.togglers.include(toggler);
        this.elements.include(element);

        var togglers = this.togglers,
            options = this.options,
            test = togglers.contains(toggler),
            idx = togglers.indexOf(toggler),
            displayer = this.display.pass(idx, this);

        toggler.store('accordion:display', displayer)
            .addEvent(options.trigger, displayer);

        if (options.height) element.setStyles({'padding-top': 0, 'border-top': 'none', 'padding-bottom': 0, 'border-bottom': 'none'});
        if (options.width) element.setStyles({'padding-left': 0, 'border-left': 'none', 'padding-right': 0, 'border-right': 'none'});

        element.fullOpacity = 1;
        if (options.fixedWidth) element.fullWidth = options.fixedWidth;
        if (options.fixedHeight) element.fullHeight = options.fixedHeight;
        element.setStyle('overflow', 'hidden');

        if (!test) for (var fx in this.effects) {
            element.setStyle(fx, 0);
        }
        return this;
    },

    removeSection: function (toggler, displayIndex) {
        var togglers = this.togglers,
            idx = togglers.indexOf(toggler),
            element = this.elements[idx];

        var remover = function () {
            togglers.erase(toggler);
            this.elements.erase(element);
            this.detach(toggler);
        }.bind(this);

        if (this.now == idx || displayIndex != null) {
            this.display(displayIndex != null ? displayIndex : (idx - 1 >= 0 ? idx - 1 : 0)).chain(remover);
        } else {
            remover();
        }
        return this;
    },

    detach: function (toggler) {
        var remove = function (toggler) {
            toggler.removeEvent(this.options.trigger, toggler.retrieve('accordion:display'));
        }.bind(this);

        if (!toggler) this.togglers.each(remove);
        else remove(toggler);
        return this;
    },

    display: function (index, useFx) {
        if (!this.check(index, useFx)) return this;

        var obj = {},
            elements = this.elements,
            options = this.options,
            effects = this.effects;

        if (useFx == null) useFx = true;
        if (typeOf(index) == 'element') index = elements.indexOf(index);
        if (index == this.previous && !options.alwaysHide) return this;

        if (options.resetHeight) {
            var prev = elements[this.previous];
            if (prev && !this.selfHidden) {
                for (var fx in effects) prev.setStyle(fx, prev[effects[fx]]);
            }
        }

        if ((this.timer && options.link == 'chain') || (index === this.previous && !options.alwaysHide)) return this;

        this.previous = index;
        this.selfHidden = false;

        elements.each(function (el, i) {
            obj[i] = {};
            var hide;
            if (i != index) {
                hide = true;
            } else if (options.alwaysHide && ((el.offsetHeight > 0 && options.height) || el.offsetWidth > 0 && options.width)) {
                hide = true;
                this.selfHidden = true;
            }
            this.fireEvent(hide ? 'background' : 'active', [this.togglers[i], el]);
            for (var fx in effects) obj[i][fx] = hide ? 0 : el[effects[fx]];
            if (!useFx && !hide && options.resetHeight) obj[i].height = 'auto';
        }, this);

        this.internalChain.clearChain();
        this.internalChain.chain(function () {
            if (options.resetHeight && !this.selfHidden) {
                var el = elements[index];
                if (el) el.setStyle('height', 'auto');
            }
        }.bind(this));

        return useFx ? this.start(obj) : this.set(obj).internalChain.callChain();
    }

});



