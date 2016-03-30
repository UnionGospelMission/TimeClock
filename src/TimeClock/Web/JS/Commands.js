// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock

"use strict";

TimeClock.Commands = Nevow.Athena.Widget.subclass("TimeClock.Commands");
TimeClock.Commands.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */
    function __init__(self, node){
        TimeClock.Commands.upcall(self, "__init__", node);
        //self.callRemote("getVisibility");
    },
    function runCommand(self, node){
        var args = self.getArgs(node);
        console.log(args);
        console.log(self.callRemote('runCommand', args));
        return false;
    },
    function hide(self){
        self.node.style.display="none";
    },
    function show(self){
        self.node.style.display="block";
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

