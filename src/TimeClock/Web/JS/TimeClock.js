// import Nevow.Athena
// import Divmod.Runtime
// import redirect

TimeClock.MenuPane = Nevow.Athena.Widget.subclass("TimeClock.MenuPane");
TimeClock.MenuPane.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */
    function menuClicked(self, node){
        self.callRemote('navigate', node.id.split("-")[1]);
    },
    function hideClockIn(self){
        self.nodeById("clockIn").style.display='none';
        self.nodeById("clockOut").style.display='block';
    },
    function hideClockOut(self){
        self.nodeById("clockOut").style.display='none';
        var nbi = self.nodeById("clockIn");
        if (nbi){
            nbi.style.display='block';
        }
    }

);


TimeClock.ActionPane = Nevow.Athena.Widget.subclass("TimeClock.ActionPane");
TimeClock.ActionPane.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */

);
