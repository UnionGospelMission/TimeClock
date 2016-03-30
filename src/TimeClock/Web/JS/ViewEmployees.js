// import TimeClock.Commands

"use strict";

TimeClock.ViewEmployees = TimeClock.Commands.subclass("TimeClock.ViewEmployees");
TimeClock.ViewEmployees.methods(
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
    }
);
