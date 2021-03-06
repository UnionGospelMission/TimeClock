// import TimeClock.Widgets
'use strict';

TimeClock.Widgets.ListToListSelector = TimeClock.Widgets.subclass("TimeClock.Widgets.SaveList");
TimeClock.Widgets.ListToListSelector.methods(
    function __init__(self, node){
        TimeClock.Widgets.ListToListSelector.upcall(self, '__init__', node);
        self.node.style.display='block';
        setTimeout(function(){
            self.childWidgets[1].node.style.display='inline-block';
            self.childWidgets[1].node.style.float='left';
            self.childWidgets[0].node.style.display='inline-block';
            self.childWidgets[0].node.style.float='left';
            self.node.style.display='flex';
        },100);

    },
    function listClicked(self, node, evt){
        var e = window.event || evt;
        var l1 = self.childWidgets[0];
        var l2 = self.childWidgets[1];
        var t = TimeClock.get(e.target);
        if (t.widgetParent===l1){
            self.refresh();
        }
        e.stopPropagation();
    },
    function doSave(self, node, evt){
        var event = window.event || evt;
        var args = [];
        var selected = self.childWidgets[1].getSelected();
        console.log(25, selected);
        for (var idx=0; idx<selected.length;idx++){
            args.push(Nevow.Athena.athenaIDFromNode(selected[idx].node));
        }
        self.callRemote('doSave', args);
    },
    function refresh(self){
        var l1 = self.childWidgets[0];
        var l2 = self.childWidgets[1];
        var selected = l1.getSelected();
        if (selected.length>0){
            self.busyCallRemote("targetChanged", Nevow.Athena.athenaIDFromNode(selected[0].node)).addCallback(function(args){
                var l = args[0];
                var b = args[1];
                l2.select(l, b);
            });
        }
    }
);
