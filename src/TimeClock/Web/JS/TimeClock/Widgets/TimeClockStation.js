// import TimeClock.Commands
// import redirect
'use strict';

TimeClock.Widgets.TimeClockStation = TimeClock.Commands.subclass("TimeClock.Widgets.TimeClockStation");
TimeClock.Widgets.TimeClockStation.methods(
    function start(self, node, evt) {
        self.callRemote('start').addCallback(function(pageId) {
            $.redirectPost("/", {pageId: pageId});
        });

    }
);
