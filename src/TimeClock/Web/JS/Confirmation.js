// import TimeClock.Commands

"use strict";

TimeClock.Confirmation = TimeClock.Commands.subclass("TimeClock.Confirmation");
TimeClock.Confirmation.methods(
    function confirm(self, node){
        self.busyCallRemote("confirm");
        if (self.callback){
            self.callback();
        }

        self.onClose();
    }
);
