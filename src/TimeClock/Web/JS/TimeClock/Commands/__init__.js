// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock

"use strict";
TimeClock.Commands = TimeClock.subclass("TimeClock.Commands");
TimeClock.Commands.methods(
    function __init__(self, node){
        TimeClock.Commands.upcall(self, "__init__", node);
        if (self.node.dataset.toplevel){
            TimeClock.ActionPane.fromAthenaID(2).commands[self.node.dataset.name] = self;
        }
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
    function getArgs(self, node){
        return $(node).serializeArray();
    }


);


