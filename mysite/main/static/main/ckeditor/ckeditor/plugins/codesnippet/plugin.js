﻿/*
 Copyright (c) 2003-2015, CKSource - Frederico Knabben. All rights reserved.
 For licensing, see LICENSE.md or http://ckeditor.com/license
*/
(function() {
    function d(a) {
        CKEDITOR.tools.extend(this, a);
        this.queue = [];
        this.init ? this.init(CKEDITOR.tools.bind(function() {
            for (var a; a = this.queue.pop();) a.call(this);
            this.ready = !0
        }, this)) : this.ready = !0
    }

    function l(a) {
        var b = a.config.codeSnippet_codeClass,
            c = /\r?\n/g,
            h = new CKEDITOR.dom.element("textarea");
        a.widgets.add("codeSnippet", {
            allowedContent: "pre; code(language-*)",
            requiredContent: "pre",
            styleableElements: "pre",
            template: '<pre><code class="' + b + '"></code></pre>',
            dialog: "codeSnippet",
            pathName: a.lang.codesnippet.pathName,
            mask: !0,
            parts: {
                pre: "pre",
                code: "code"
            },
            highlight: function() {
                var e = this,
                    f = this.data,
                    b = function(a) {
                        e.parts.code.setHtml(k ? a : a.replace(c, "<br>"))
                    };
                b(CKEDITOR.tools.htmlEncode(f.code));
                a._.codesnippet.highlighter.highlight(f.code, f.lang, function(e) {
                    a.fire("lockSnapshot");
                    b(e);
                    a.fire("unlockSnapshot")
                })
            },
            data: function() {
                var a = this.data,
                    b = this.oldData;
                a.code && this.parts.code.setHtml(CKEDITOR.tools.htmlEncode(a.code));
                b && a.lang != b.lang && this.parts.code.removeClass("language-" + b.lang);
                a.lang && (this.parts.code.addClass("language-" +
                    a.lang), this.highlight());
                this.oldData = CKEDITOR.tools.copy(a)
            },
            upcast: function(e, f) {
                if ("pre" == e.name) {
                    for (var c = [], d = e.children, i, j = d.length - 1; 0 <= j; j--) i = d[j], (i.type != CKEDITOR.NODE_TEXT || !i.value.match(m)) && c.push(i);
                    var g;
                    if (!(1 != c.length || "code" != (g = c[0]).name))
                        if (!(1 != g.children.length || g.children[0].type != CKEDITOR.NODE_TEXT)) {
                            if (c = a._.codesnippet.langsRegex.exec(g.attributes["class"])) f.lang = c[1];
                            h.setHtml(g.getHtml());
                            f.code = h.getValue();
                            g.addClass(b);
                            return e
                        }
                }
            },
            downcast: function(a) {
                var c =
                    a.getFirst("code");
                c.children.length = 0;
                c.removeClass(b);
                c.add(new CKEDITOR.htmlParser.text(CKEDITOR.tools.htmlEncode(this.data.code)));
                return a
            }
        });
        var m = /^[\s\n\r]*$/
    }
    var k = !CKEDITOR.env.ie || 8 < CKEDITOR.env.version;
    CKEDITOR.plugins.add("codesnippet", {
        requires: "widget,dialog",
        lang: "ar,bg,ca,cs,da,de,el,en,en-gb,eo,es,et,fa,fi,fr,fr-ca,gl,he,hr,hu,it,ja,km,ko,ku,lt,lv,nb,nl,no,pl,pt,pt-br,ro,ru,sk,sl,sq,sv,th,tr,tt,ug,uk,vi,zh,zh-cn",
        icons: "codesnippet",
        hidpi: !0,
        beforeInit: function(a) {
            a._.codesnippet = {};
            this.setHighlighter = function(b) {
                a._.codesnippet.highlighter = b;
                b = a._.codesnippet.langs = a.config.codeSnippet_languages || b.languages;
                a._.codesnippet.langsRegex = RegExp("(?:^|\\s)language-(" + CKEDITOR.tools.objectKeys(b).join("|") + ")(?:\\s|$)")
            }
        },
        onLoad: function() {
            CKEDITOR.dialog.add("codeSnippet", this.path + "dialogs/codesnippet.js")
        },
        init: function(a) {
            a.ui.addButton && a.ui.addButton("CodeSnippet", {
                label: a.lang.codesnippet.button,
                command: "codeSnippet",
                toolbar: "insert,10"
            })
        },
        afterInit: function(a) {
            var b =
                this.path;
            l(a);
            a._.codesnippet.highlighter || this.setHighlighter(new CKEDITOR.plugins.codesnippet.highlighter({
                languages: {
                    cpp: "C++",
                    cs: "C#",
                    css: "CSS",
                    html: "HTML",
                    ini: "INI",
                    lua: "Lua",
                    javascript: "JavaScript",
                    json: "JSON",
                    php: "PHP",
                    python: "Python",
                    sql: "SQL",
                    xml: "XML"
                },
                init: function(c) {
                    var h =
                        this;
                    k && CKEDITOR.scriptLoader.load(b + "lib/highlight/highlight.pack.js", function() {
                        h.hljs = window.hljs;
                        c()
                    });
                    a.addContentsCss && a.addContentsCss(b + "lib/highlight/styles/" + a.config.codeSnippet_theme + ".css")
                },
                highlighter: function(a, b, d) {
                    (a = this.hljs.highlightAuto(a, this.hljs.getLanguage(b) ? [b] : void 0)) && d(a.value)
                }
            }))
        }
    });
    CKEDITOR.plugins.codesnippet = {
        highlighter: d
    };
    d.prototype.highlight = function() {
        var a = arguments;
        this.ready ? this.highlighter.apply(this, a) : this.queue.push(function() {
            this.highlighter.apply(this,
                a)
        })
    }
})();
CKEDITOR.config.codeSnippet_codeClass = "hljs";
CKEDITOR.config.codeSnippet_theme = "default";