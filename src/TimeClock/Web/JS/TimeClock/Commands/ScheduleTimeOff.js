// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands

"use strict";
TimeClock.Commands.ScheduleTimeOff = TimeClock.Commands.subclass("TimeClock.Commands.ScheduleTimeOff");
TimeClock.Commands.ScheduleTimeOff.methods(
    function __init__(self, node){
        TimeClock.Commands.ScheduleTimeOff.upcall(self, '__init__', node);
        var options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            showTimezone: true,
            timezoneList: [
                { value: "AUTO",  label: 'AUTO' },
                { value: 'PDT', label: 'PDT'},
                    { value: 'PST',  label: 'PST' }
            ]
        };
        $(self.nodeById('startTime')).datetimepicker(options);
        //$(self.nodeById('endTime')).(options);
    },
    function scheduleTimeOff(self, node) {
        self.busyCallRemote('scheduleTimeOff', self.nodeById('startTime').value, self.nodeById('endTime').value);
    }
);


