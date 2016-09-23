// import TimeClock.Commands

"use strict";
TimeClock.Commands.ViewReports = TimeClock.Commands.subclass("TimeClock.Commands.ViewReports");
TimeClock.Commands.ViewReports.methods(
    function __init__(self, node){
        TimeClock.Commands.ViewReports.upcall(self, '__init__', node);
    },
    function newReport(self, node) {
        self.busyCallRemote('newReport');
    }
);


