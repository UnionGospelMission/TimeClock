// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock

"use strict";

TimeClock.Commands = Nevow.Athena.Widget.subclass("TimeClock.Commands");
TimeClock.Commands.methods(
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
        var oldstyle = document.body.style.cursor;
        document.body.style.cursor='progress';
        return function(data){
            document.body.style.cursor=oldstyle;
            return data;
        };
    },
    function __init__(self, node){
        TimeClock.Commands.upcall(self, "__init__", node);
        TimeClock.ActionPane.fromAthenaID(2).commands[self.node.dataset.name] = self;
        if (node.style.display!='none' && node.dataset.name){
            TimeClock.ActionPane.fromAthenaID(2).currentCommand = self;
        }

    },
    function runCommand(self, node){
        var args = self.getArgs(node);
        var b = self.setBusy();
        self.busyCallRemote('runCommand', args).addCallback(b);

        return false;
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
    function getArgs(self, node){
        return $(node).serializeArray();
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

    }


);


