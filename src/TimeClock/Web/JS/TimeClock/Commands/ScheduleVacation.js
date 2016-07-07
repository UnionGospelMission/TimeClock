// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands

"use strict";
TimeClock.Commands.ScheduleVacation = TimeClock.Commands.subclass("TimeClock.Commands.ScheduleVacation");
TimeClock.Commands.ScheduleVacation.methods(
    function __init__(self, node){
        TimeClock.Commands.ScheduleVacation.upcall(self, '__init__', node);
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
        $(self.nodeById('endTime')).datetimepicker(options);
    },
    function scheduleVacation(self, node) {
        self.busyCallRemote('scheduleVacation', self.nodeById('startTime').value, self.nodeById('endTime').value);
    }
);


