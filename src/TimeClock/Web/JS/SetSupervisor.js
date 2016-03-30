// import TimeClock.Commands

"use strict";

TimeClock.SetSupervisor = TimeClock.Commands.subclass("TimeClock.SetSupervisor");
TimeClock.SetSupervisor.methods(
    function runCommand(self, node) {
        self.callRemote('runCommand', self.getArgs(node));
        event.preventDefault();
    },
    function setSup(self, val){
        self.nodeById("supervisorID").value = val;

    },
    function setEmp(self, val){
        self.nodeById("employeeID").value = val;
    },
    function runCommand(self, node){
        self.callRemote("runCommand", [self.nodeById("employeeID").value, self.nodeById("supervisorID").value]);
        event.preventDefault();
    },
    function runRefresh(self, node){
        self.callRemote("refresh");
    },
    function refreshLists(self, suplist, emplist){
        self.addChildWidgetFromWidgetInfo(emplist).addCallback(
                function childAdded(widget){
                    self.childWidgets[0].replaceSelf(widget.node);
                }
            );
        self.addChildWidgetFromWidgetInfo(suplist).addCallback(
                function childAdded(widget){
                    self.childWidgets[0].replaceSelf(widget.node);
                }
            );
    }
);
