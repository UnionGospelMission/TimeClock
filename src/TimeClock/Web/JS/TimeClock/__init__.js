// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import arrayRemove
// import jquery
// import jquery.ui

"use strict";

$.ui.dialog.prototype._focusTabbable = $.noop;

window.TimeClock = Nevow.Athena.Widget.subclass("TimeClock");
TimeClock.methods(
    function busyCallRemote(self, func){
        var busy = self.setBusy();
        var args = [func];
        for (var idx=2; idx<arguments.length;idx++){
            args.push(arguments[idx]);
        }
        var cb = self.callRemote.apply(self, args);
        cb.addCallback(busy);
        cb.addErrback(busy);
        return cb;
    },
    function setBusy(self){
        TimeClock.busyCount++;
        document.body.style.cursor='progress';
        var d = $('<div>processing...</div>').dialog({
            closeOnEscape:false,
            dialogClass: "no-close"
            }
        );
        return function notbusy(data){
            if (--TimeClock.busyCount<1){
                document.body.style.cursor=TimeClock.oldstyle;
            }
            d.dialog('close');
            return data;
        };

    },
    function __init__(self, node){
        TimeClock.busyCount = 0;
        TimeClock.oldstyle = "";
        TimeClock.upcall(self, "__init__", node);
    },
    function hide(self){
        self.node.style.display="none";
        if (self.d1 != undefined){
            $(self.d1).hide();
        }
    },
    function show(self){
        self.node.style.display="block";
        if (self.node.dataset.title){
            document.title = self.node.dataset.title;
        }
        if (self.d1 != undefined){
            $(self.d1).show();
        }
    },
    function onClose(self, node){
        if (self.node && self.node.parentNode) {
            self.node.parentNode.removeChild(self.node);
        }
        if (self.widgetParent){
            self.widgetParent.removeChildWidget(self);
        }
    },
    function replaceSelf(self, node){
        self.node.parentNode.replaceChild(node, self.node);
        if (self.widgetParent){
            self.widgetParent.removeChildWidget(self);
        }

    },
    function dialog(self, node, closeable){
        if (closeable){
            var buttons = [
                {
                    text: "OK",
                    click: function() {
                        $( this ).dialog( "close" );
                    }
                }
            ]
        }
        else {
            var buttons = [];
        }
        return $(node).dialog({
            dialogClass: "no-close",
            buttons: buttons
        });
    }


);


if (!String.prototype.format) {
    String.prototype.format = function() {
        var str, args, arg

        str = this.toString();
        if (!arguments.length)
            return str;

        args = typeof arguments[0];
        args = (("string" == args || "number" == args) ? arguments : arguments[0]);

        for (arg in args)
            str = str.replace(RegExp("\\{" + arg + "\\}", "gi"), args[arg]);
        return str;
    }
}

window.getCookie = function getCookie(name) {
  var match = document.cookie.match(new RegExp(name + '=([^;]+)'));
  if (match) return match[1];
};
