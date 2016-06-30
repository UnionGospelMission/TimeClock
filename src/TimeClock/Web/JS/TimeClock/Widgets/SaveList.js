// import TimeClock.Widgets
'use strict';

TimeClock.Widgets.SaveList = TimeClock.Widgets.subclass("TimeClock.Widgets.SaveList");
TimeClock.Widgets.SaveList.methods(
    function saveAll(self, node, evt){
        var e = window.event || evt;
        var widgets = self.widgetParent.getAll();
        for (var idx=0;idx<widgets.length;){
            var w = widgets[idx++];
            var s = TimeClock.get(w.elm);
            if (s==self){
                continue;
            }
            s.saveClicked(node, e);
        }
    }
);
