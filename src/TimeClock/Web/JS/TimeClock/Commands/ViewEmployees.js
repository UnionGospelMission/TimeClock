// import TimeClock.Commands

"use strict";
TimeClock.Commands.ViewEmployees = TimeClock.Commands.subclass("TimeClock.Commands.ViewEmployees");
TimeClock.Commands.ViewEmployees.methods(
    function refresh(self, node) {
        self.busyCallRemote('reload', self.nodeById('showActive').checked, self.nodeById('showInactive').checked);
    }
);


