// import TimeClock
// import jquery
// import jquery.ui.datetimepicker

"use strict";


TimeClock.Objects.TimeEntryRenderer = TimeClock.Objects.subclass("TimeClock.Objects.TimeEntryRenderer");
TimeClock.Objects.TimeEntryRenderer.methods(
    function __init__(self, node){
        console.log(11);
        TimeClock.Objects.TimeEntryRenderer.upcall(self, "__init__", node);
        console.log(13);
        var options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            showTimezone: true,
            timezoneList: [
                { value: 'PDT', label: 'PDT'},
                { value: 'PST', label: 'PST'}
            ]
        };
        setTimeout(function(){$(self.nodeById('startTime')).datetimepicker(options);}, 500);
        setTimeout(function(){$(self.nodeById('endTime')).datetimepicker(options);}, 500);
        console.log(16);
    }

);
