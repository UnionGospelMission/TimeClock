// import TimeClock.Commands

"use strict";

TimeClock.ApproveTime = TimeClock.Commands.subclass("TimeClock.ApproveTime");
TimeClock.ApproveTime.methods(
    function runCommand(self, node){
        self.callRemote('runCommand', self.getArgs(node)).addCallback(
            function(newNode){
                self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.hours = widget;
                        self.node.appendChild(widget.node);
                        self.nodeById("Submit").style.display="block";
                    }
                );
            }
        );
        return false;
    },
    function getArgs(self, node){
        window.node=node;
        return [node.startDate.valueAsDate.toISOString(),
                node.startDate.valueAsDate.getTimezoneOffset(),
                node.endDate.valueAsDate.toISOString(),
                node.endDate.valueAsDate.getTimezoneOffset(),
                node.employeeID.value];
    },
    function approveTime(self, node){
        var args = [];
        for (var idx=0; idx < self.hours.selected.length; idx++){
            console.log(32, self.hours.selected[idx]);
            args.push(self.hours.selected[idx].dataset.ordinal);
        }
        self.callRemote("approveShifts", args).addCallback(function(retval){
            self.nodeById("Submit").style.display="none";
        });
    },
    function selectEmployee(self, emp_id){
        self.nodeById("employeeID").value=emp_id;
        self.nodeById("employeeID").style.display="block";
    }
);
