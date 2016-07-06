// import TimeClock.Commands

"use strict";
TimeClock.Commands.ViewReports = TimeClock.Commands.subclass("TimeClock.Commands.ViewReports");
TimeClock.Commands.ViewReports.methods(
    function newReport(self, node) {
        self.busyCallRemote('newReport');
    }
);


