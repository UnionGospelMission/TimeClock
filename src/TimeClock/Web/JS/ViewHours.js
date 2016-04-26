// import TimeClock.Commands
// import jquery_ui
// import Modernizr
'use strict';


TimeClock.ViewHours = TimeClock.Commands.subclass("TimeClock.ViewHours");
TimeClock.ViewHours.methods(
    function __init__(self, node){
        TimeClock.Commands.upcall(self, "__init__", node);
        if (!Modernizr.inputtypes.date){
            self.startDate = $(self.nodeByAttribute('name', 'startDate')).datepicker({ dateFormat: 'yy-mm-dd' });
            self.endDate = $(self.nodeByAttribute('name', 'endDate')).datepicker({ dateFormat: 'yy-mm-dd' });

        }


    },
    function runCommand(self, node){
        self.busyCallRemote('runCommand', self.getArgs(node)).addCallback(
            function(newNode){
                self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.node.appendChild(widget.node);
                    }
                );
            }
        );
        return false;
    },
    function getArgs(self, node){
        var startDate;
        var endDate;
        if (Modernizr.inputtypes.date){
            startDate = node.startDate.valueAsDate.toISOString();
            endDate =  node.endDate.valueAsDate.toISOString();
        }
        else{
            var tzoffset = new Date().getTimezoneOffset();
            startDate = $(node.startDate).datepicker('getDate').toISOString();
            endDate = $(node.endDate).datepicker('getDate').toISOString();
            console.log(startDate, endDate);
        }

        return [startDate, endDate];
    }
);
