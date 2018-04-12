// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands
// import jquery.ui.datetimepicker

"use strict";
TimeClock.Commands.ApproveDepartmentTime = TimeClock.Commands.subclass("TimeClock.Commands.ApproveDepartmentTime");
TimeClock.Commands.ApproveDepartmentTime.methods(
    function __init__(self, node){
        TimeClock.Commands.ApproveShifts.upcall(self, '__init__', node);
        var options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            timezone: 'AUTO',
            showTimezone: true,
            timezoneList: [
                { value: 'PDT', label: 'PDT'},
                    { value: 'PST',  label: 'PST' },
                    { value: "AUTO",  label: 'AUTO' }
            ],
            onSelect: function(){self.startTimeChanged();}
        };
        self.nodeByAttribute("name", "save").style.display='none';
        $(self.nodeById('startTime')).datetimepicker(options);
        options.hour = 23;
        options.minute = 59;
        options.second = 59;
        options.onSelect = function(){self.endTimeChanged();};
        $(self.nodeById('endTime')).datetimepicker(options);
        self.timer = 0;
    },
    function startTimeChanged(self, node) {
        self.busyCallRemote("startTimeChanged", self.nodeById('startTime').value);
    },
    function endTimeChanged(self, node) {
        self.busyCallRemote("endTimeChanged", self.nodeById('endTime').value);
    }
);


