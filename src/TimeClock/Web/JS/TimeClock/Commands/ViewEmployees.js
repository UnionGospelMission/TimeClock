// import TimeClock.Commands
// import TimeClock.Commands.SetPassword

"use strict";
TimeClock.Commands.ViewEmployees = TimeClock.Commands.subclass("TimeClock.Commands.ViewEmployees");
TimeClock.Commands.ViewEmployees.methods(
    function __init__(self, node){
        TimeClock.Commands.ViewEmployees.upcall(self, '__init__', node);
    },
    function refresh(self, node) {
        self.busyCallRemote('reload', self.nodeById('showActive').checked, self.nodeById('showInactive').checked);
    }
);


