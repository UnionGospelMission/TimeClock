// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands

"use strict";
TimeClock.Commands.ApproveShifts = TimeClock.Commands.subclass("TimeClock.Commands.ApproveShifts");
TimeClock.Commands.ApproveShifts.methods(
    function __init__(self, node){
        TimeClock.Commands.ApproveShifts.upcall(self, '__init__', node);
        self.nodeByAttribute("name", "save").style.display='none';
    }
);


