// import TimeClock
// import jquery
// import jquery.ui.datetimepicker

"use strict";


TimeClock.Objects.TimeEntryRenderer = TimeClock.Objects.subclass("TimeClock.Objects.TimeEntryRenderer");
TimeClock.Objects.TimeEntryRenderer.methods(
    function __init__(self, node){
        TimeClock.Objects.TimeEntryRenderer.upcall(self, "__init__", node);

        setTimeout(function(){
            try {
                self.setDateTimePicker(self.nodeById('startTime'));
                self.setDateTimePicker(self.nodeById('endTime'));
            }
            catch (e) {

            }
        }, 500);

    },
    function newValues(self, args) {
        TimeClock.Objects.TimeEntryRenderer.upcall(self, 'newValues', args);
        try {
            self.setDateTimePicker(self.nodeById('startTime'));
            self.setDateTimePicker(self.nodeById('endTime'));
        }
        catch (e) {

        }

    },
    function setDateTimePicker(self, node){
        var options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            showTimezone: true,
            timezoneList: [
            ]
        };
        var val = node.value.split(' ');
        switch (val[val.length-1]){
            case 'PDT':
                options.timezoneList = [
                    { value: 'PDT', label: 'PDT'},
                    { value: 'PST',  label: 'PST' },
                    { value: "AUTO",  label: 'AUTO' }
                ];
                break;
            case 'PST':
                options.timezoneList = [
                    { value: 'PST',  label: 'PST' },
                    { value: 'PDT', label: 'PDT'},
                    { value: "AUTO",  label: 'AUTO' }
                ];
                break;
        }
        $(node).datetimepicker(options);
    }
);
