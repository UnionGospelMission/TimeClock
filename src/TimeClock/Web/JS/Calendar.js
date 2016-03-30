// import Nevow.Athena
// import Divmod.Runtime
// import redirect

"use strict";

CommandRenderer.Commands = Nevow.Athena.Widget.subclass("CommandRenderer.Commands");
CommandRenderer.Commands.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */
    function __init__(self, node){
        CommandRenderer.Commands.upcall(self, "__init__", node);
        //self.callRemote("getVisibility");
    },
    function runCommand(self, node){
        self.callRemote('runCommand', $(node).serializeArray());
        return false;
    },
    function hide(self){
        self.node.style.display="none";
    },
    function show(self){
        self.node.style.display="block";
    }

);

