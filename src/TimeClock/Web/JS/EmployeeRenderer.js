// import CommandRenderer

"use strict";

ViewHoursRenderer.ViewHours = CommandRenderer.Commands.subclass("ViewHoursRenderer.ViewHours");
ViewHoursRenderer.ViewHours.methods(
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
