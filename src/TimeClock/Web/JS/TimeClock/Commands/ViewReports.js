// import TimeClock.Commands

"use strict";
TimeClock.Commands.ViewReports = TimeClock.Commands.subclass("TimeClock.Commands.ViewReports");
TimeClock.Commands.ViewReports.methods(
    function __init__(self, node){
        TimeClock.Commands.ViewReports.upcall(self, '__init__', node);
        self.clearLog();
    },
    function newReport(self, node) {
        self.busyCallRemote('newReport');
    },
    function progress(self, progress) {
        self.pb.progressbar({value: progress});
    },
    function log(self, msg) {
        var m = document.createElement('pre');
        m.innerHTML = msg;
        self.nodeById('log').appendChild(m);
    },
    function clearLog(self) {
        var log = self.nodeById('log');
        while (log.firstChild) {
            log.removeChild(log.firstChild);
        }
        self.pb = document.createElement('div');
        log.appendChild(self.pb);
        self.pb = $(self.pb);
    }
);


