// import TimeClock.Commands

"use strict";

TimeClock.ViewHours = TimeClock.Commands.subclass("TimeClock.ViewHours");
TimeClock.ViewHours.methods(
    function runCommand(self, node){
        self.callRemote('runCommand', self.getArgs(node)).addCallback(
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
        window.node=node;
        window.self=self;
        return [node.startDate.valueAsDate.toISOString(), node.endDate.valueAsDate.toISOString()];
    }
);
