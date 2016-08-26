// import TimeClock.TimeClockStation
// import jquery.ui
'use strict';

TimeClock.TimeClockStation.Action = TimeClock.TimeClockStation.subclass("TimeClock.TimeClockStation.Action");
TimeClock.TimeClockStation.Action.methods(
    function __init__(self, node) {
        TimeClock.TimeClockStation.Action.upcall(self, '__init__', node);
        var doptions = {
            dialogClass: "no-close",
            closeOnEscape: false,
            position: { my: "left top", at: "center top", of: window, collision: "fit"}

        };
        setTimeout(function() {
            var d = $(self.childWidgets[1].node).dialog(doptions);
            doptions.position.at='right top';
            doptions.position.of=d;
            $(self.childWidgets[2].node).dialog(doptions);
            self.childWidgets[1].nodeByAttribute('value', 'Close').style.display='none';
            self.childWidgets[2].nodeByAttribute('value', 'Close').style.display='none';
        }, 1);
        document.body.onclick = function(evt) {
            self.listClicked(null, evt);
        }
    },
    function listClicked(self, node, evt) {
        var e = window.event || evt;
        var t = TimeClock.get(e.target);
        var cInOut = self.childWidgets[0];
        var cIn = self.childWidgets[1];
        var cOut = self.childWidgets[2];
        if (t && t.widgetParent.widgetParent===cIn) {
            cOut.childWidgets[0].select([]);
            cInOut.showOut(t);
        }
        else if (t && t.widgetParent.widgetParent===cOut){
            cIn.childWidgets[0].select([]);
            cInOut.showIn(t);
        }
    }
);
