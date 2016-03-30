// import TimeClock.Commands

"use strict";

TimeClock.WorkLocation = TimeClock.Commands.subclass("TimeClock.WorkLocation");
TimeClock.WorkLocation.methods(
    function setEmp(self, val, selected){
        self.nodeById("employeeID").value = val;
        self.childWidgets[1].select(selected);
    },
    function runCommand(self, node){
        var selected = [];
        for (var idx=0;idx<self.childWidgets[1].selected.length; idx++){
            selected.push(self.childWidgets[1].selected[idx].cells[1].innerHTML);
        }
        self.callRemote("runCommand", [self.nodeById("employeeID").value, selected]);
        event.preventDefault();
    },
    function runRefresh(self, node){
        self.callRemote("refresh");
    },
    function loadEmployeeList(self, node){
        self.callRemote("loadEmployeeList").addCallback(function(emplist){
            self.addChildWidgetFromWidgetInfo(emplist).addCallback(
                function childAdded(widget){
                    node.parentNode.replaceChild(widget.node, node);
                    self.childWidgets.reverse();
                }
            );
        });

    },
    function refreshLists(self, emplist, wrkloclist){
        self.addChildWidgetFromWidgetInfo(emplist).addCallback(
                function childAdded(widget){
                    self.childWidgets[0].replaceSelf(widget.node);
                }
            );
        self.addChildWidgetFromWidgetInfo(wrkloclist).addCallback(
                function childAdded(widget){
                    self.childWidgets[0].replaceSelf(widget.node);
                }
            );
    }
);
