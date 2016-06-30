// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock

"use strict";

TimeClock.Calendar = Nevow.Athena.Widget.subclass("TimeClock.Calendar");
TimeClock.Calendar.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */
    function __init__(self, node){
        TimeClock.Calendar.upcall(self, "__init__", node);
        self.selected = [];
    },
    function hide(self){
        self.node.style.display="none";
    },
    function show(self){
        self.node.style.display="block";
    },
    function dayClicked(self, node){
        if (self.selected.includes(node)){
            self.selected.pop(node);
            node.style.backgroundColor="white";
        }
        else{
            self.selected.push(node);
            node.style.backgroundColor="teal";
        }
    },
    function dayDblClicked(self, node) {

        self.callRemote("zoomOnDay", node.dataset.ordinal).addCallback(
            function (newNode) {
                self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget) {
                        self.node.appendChild(widget.node);
                    }
                );
            }
        );
    },
    function onClose(self, node){
        self.node.parentNode.removeChild(self.node);
    }

);

