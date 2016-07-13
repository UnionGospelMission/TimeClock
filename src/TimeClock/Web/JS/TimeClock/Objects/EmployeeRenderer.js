// import TimeClock.Objects
// import jquery


"use strict";


TimeClock.Objects.EmployeeRenderer = TimeClock.Objects.subclass("TimeClock.Objects.EmployeeRenderer");
TimeClock.Objects.EmployeeRenderer.methods(
    function __init__(self, node){
        TimeClock.Objects.EmployeeRenderer.upcall(self, '__init__', node);
        if (self.node.dataset.toplevel){
            TimeClock.ActionPane.fromAthenaID(2).commands["myProfile"] = self;
        }
        if (node.style.display!='none' && node.dataset.name){
            TimeClock.ActionPane.fromAthenaID(2).currentCommand = self;
        }
    },
    function actionsClicked(self, node, evt){
        var event = window.event || evt;
        event.stopPropagation();
        self.nodeById('employeeActions').style.display = self.nodeById('employeeActions').style.display=='block' ? 'none' : 'block';

    }


);
