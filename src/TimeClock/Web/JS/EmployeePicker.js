// import TimeClock.Commands

"use strict";

TimeClock.EmployeePicker = TimeClock.Commands.subclass("TimeClock.EmployeePicker");
TimeClock.EmployeePicker.methods(
    function pickEmployee(self, node) {
        var lst = self.childWidgets[0];
        var args = [];
        for (var idx = 0; idx < lst.selected.length; idx++) {
            args.push(lst.selected[idx].children[0].dataset.index);
        }
        self.callRemote('runCallback', args);
    },
    function loadEmployeeList(self, node){
        node.disabled=true;
        self.callRemote("loadEmployeeList").addCallback(function(elist){
            self.addChildWidgetFromWidgetInfo(elist).addCallback(function(widget){
                node.parentNode.replaceChild(widget.node, node);
            });

        });
    }

);
