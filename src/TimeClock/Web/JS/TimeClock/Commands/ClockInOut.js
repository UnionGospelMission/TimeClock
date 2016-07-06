// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock
// import TimeClock.Commands

"use strict";
TimeClock.Commands.ClockInOut = TimeClock.Commands.subclass("TimeClock.Commands.ClockInOut");
TimeClock.Commands.ClockInOut.methods(
    function __init__(self, node){
        var toplevel = node.dataset.toplevel;
        self.toplevel = toplevel;
        TimeClock.Commands.ClockInOut.upcall(self, "__init__", node);
        self.node.dataset.toplevel = toplevel;
        if (toplevel){
            TimeClock.ActionPane.fromAthenaID(2).commands['clockInOut'] = self;
            TimeClock.MenuPane.fromAthenaID(1).nodeById(self.toplevel).id = 'athenaid:1-clockInOut';
            if (self.nodeById('clockin').style.display=='none'){
                TimeClock.MenuPane.fromAthenaID(1).nodeById('clockInOut').innerHTML = 'Clock Out';
            }
            else{
                TimeClock.MenuPane.fromAthenaID(1).nodeById('clockInOut').innerHTML = 'Clock In';
            }

        }

    },
    function refresh(self, subs, locs) {
        console.log(29, subs, locs);
        self.nodeById('sub').innerHTML = subs;
        self.nodeById('wloc').innerHTML = locs;
    },
    function doClockIn(self, node){
        self.callRemote("clockIn", self.nodeById("sub").value, self.nodeById("wloc").value);
    },
    function doClockOut(self, node){
        self.callRemote("clockOut");
    },
    function clockedIn(self){
        self.nodeById('clockin').style.display='none';
        self.nodeById('clockout').style.display='block';
        TimeClock.MenuPane.fromAthenaID(1).nodeById('clockInOut').innerHTML = 'Clock Out';
    },
    function clockedOut(self){
        self.nodeById('clockout').style.display='none';
        self.nodeById('clockin').style.display='block';
        TimeClock.MenuPane.fromAthenaID(1).nodeById('clockInOut').innerHTML = 'Clock In';

    }
);


