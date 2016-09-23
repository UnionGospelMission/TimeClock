// import TimeClock.Commands

"use strict";
TimeClock.Commands.CheckForNewEmployees = TimeClock.Commands.subclass("TimeClock.Commands.CheckForNewEmployees");
TimeClock.Commands.CheckForNewEmployees.methods(
    function __init__(self, node){
        TimeClock.Commands.CheckForNewEmployees.upcall(self, '__init__', node);

    },
    function runCheck(self, node) {
        self.busyCallRemote('runCheck').addCallback(function(nodeinfo){
            self.addChildWidgetFromWidgetInfo(nodeinfo).addCallback(function (widget) {
                self.node.appendChild(widget.node);
            });
        });
    }
);


