// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import arrayRemove
// import jquery
// import jquery.ui

"use strict";

TimeClock = Nevow.Athena.Widget.subclass("TimeClock");
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
        return function notbusy(data){
            if (--TimeClock.busyCount<1){
                document.body.style.cursor=TimeClock.oldstyle;
            }
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
    },
    function show(self){
        self.node.style.display="block";
        if (self.node.dataset.title){
            document.title = self.node.dataset.title;
        }

    },
    function onClose(self, node){
        self.node.parentNode.removeChild(self.node);
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
            buttons = [
                {
                    text: "OK",
                    click: function() {
                        $( this ).dialog( "close" );
                    }
                }
            ]
        }
        else {
            buttons = [];
        }
        return $(node).dialog({
            dialogClass: "no-close",
            buttons: buttons
        });
    }


);


