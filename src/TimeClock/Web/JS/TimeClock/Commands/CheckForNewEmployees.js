// import TimeClock.Commands

"use strict";
TimeClock.Commands.CheckForNewEmployees = TimeClock.Commands.subclass("TimeClock.Commands.CheckForNewEmployees");
TimeClock.Commands.CheckForNewEmployees.methods(
    function runCheck(self, node) {
        self.busyCallRemote('runCheck').addCallback(function(nodeinfo){
            self.addChildWidgetFromWidgetInfo(nodeinfo).addCallback(function (widget) {
                self.node.appendChild(widget.node);
            });
        });
    }
);


