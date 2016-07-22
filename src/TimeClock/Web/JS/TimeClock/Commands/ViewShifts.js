// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands
// import jquery.ui.datetimepicker

"use strict";
TimeClock.Commands.ViewShifts = TimeClock.Commands.subclass("TimeClock.Commands.ViewShifts");
TimeClock.Commands.ViewShifts.methods(
    function __init__(self, node){
        TimeClock.Commands.ViewShifts.upcall(self, '__init__', node);
        var options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            showTimezone: true,
            timezoneList: [
                { value: 'PDT', label: 'PDT'},
                    { value: 'PST',  label: 'PST' },
                    { value: "AUTO",  label: 'AUTO' }
            ],
            onSelect: function(){self.timeWindowChanged();}
        };
        $(self.nodeById('startTime')).datetimepicker(options);
        $(self.nodeById('endTime')).datetimepicker(options);
    },
    function timeWindowChanged(self, node){
        self.busyCallRemote("timeWindowChanged", self.nodeById('startTime').value, self.nodeById('endTime').value).addCallback(
            function newEntries(newnodes) {
                self.childWidgets[0].select(newnodes, true);
            }
        );
    }
);


