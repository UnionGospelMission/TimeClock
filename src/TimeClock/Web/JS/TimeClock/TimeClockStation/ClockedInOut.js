// import TimeClock.TimeClockStation
'use strict';

TimeClock.TimeClockStation.ClockedInOut = TimeClock.TimeClockStation.subclass("TimeClock.TimeClockStation.ClockedInOut");
TimeClock.TimeClockStation.ClockedInOut.methods(
    function __init__(self, node) {
        TimeClock.TimeClockStation.ClockedInOut.upcall(self, '__init__', node);
        var wl = document.cookie.replace(/(?:(?:^|.*;\s*)workLocation\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        var sa = document.cookie.replace(/(?:(?:^|.*;\s*)subAccount\s*\=\s*([^;]*).*$)|^.*$/, "$1");
        if (wl) {
            self.nodeById('workLocation').value = wl;
            self.selectWorkLocation(null);
        }
        if (sa) {
            self.nodeById('subAccount').value = sa;
            self.selectSubAccount(null);
        }

    },
    function showIn(self, widget) {
        self.emp = widget;
        self.nodeById('clockInOut').value="Clock In";
    },
    function showOut(self, widget) {
        self.emp = widget;
        self.nodeById('clockInOut').value="Clock Out";
    },
    function clockInOut(self, node, evt) {
        self.emp.node.style.backgroundColor='white';
        if (self.nodeById('clockInOut').value == 'Clock In') {
            self.callRemote('clockIn', Nevow.Athena.athenaIDFromNode(self.emp.node), self.nodeById('password').value)
        }
        else {
            self.callRemote('clockOut', Nevow.Athena.athenaIDFromNode(self.emp.node), self.nodeById('password').value)
        }
        self.nodeById('password').value = '';
    },
    function selectWorkLocation(self, node, evt) {
        document.cookie = 'workLocation='+self.nodeById('workLocation').value+';';
        self.callRemote("selectWorkLocation", self.nodeById('workLocation').value);
    },
    function selectSubAccount(self, node, evt) {
        document.cookie = 'subAccount='+self.nodeById('subAccount').value+';';
        self.callRemote("selectSubAccount", self.nodeById('subAccount').value);
    }
);
