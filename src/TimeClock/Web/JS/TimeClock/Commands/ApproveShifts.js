// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands
// import jquery.ui.datetimepicker

"use strict";
TimeClock.Commands.ApproveShifts = TimeClock.Commands.subclass("TimeClock.Commands.ApproveShifts");
TimeClock.Commands.ApproveShifts.methods(
    function __init__(self, node){
        TimeClock.Commands.ApproveShifts.upcall(self, '__init__', node);
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
        self.nodeByAttribute("name", "save").style.display='none';
        $(self.nodeById('startTime')).datetimepicker(options);
        $(self.nodeById('endTime')).datetimepicker(options);
        self.timer = 0;
    },
    function timeWindowChanged(self, node){
        if (self.timer==0) {
            self.timer++;
            self.busyCallRemote("timeWindowChanged", self.nodeById('startTime').value, self.nodeById('endTime').value).addCallback(
                function(){
                    self.timer=0;
                }
            );
            self.childWidgets[0].refresh();
        }
    },
    function addTime(self, node) {
        self.busyCallRemote('addTime', self.nodeById('newTimeType').value);
    }
);


