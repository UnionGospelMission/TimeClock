// import TimeClock.Commands

"use strict";


TimeClock.EmployeeRenderer = Nevow.Athena.Widget.subclass("TimeClock.EmployeeRenderer");
TimeClock.EmployeeRenderer.methods(

    function hide(self){
        self.node.style.display="none";
    },
    function show(self){
        self.node.style.display="block";
    },
    function optionsClicked(self, node){
        if (self.nodeById('employeeOptions').style.display=='block'){
            self.nodeById('employeeOptions').style.display='none';
        }
        else{
            self.nodeById('employeeOptions').style.display='block';
        }

        event.stopPropagation();
    },
    function actionsClicked(self, node){
        if (self.nodeById('employeeActions').style.display=='block'){
            self.nodeById('employeeActions').style.display='none';
        }
        else{
            self.nodeById('employeeActions').style.display='block';
        }

        event.stopPropagation();
    },
    function saveClicked(self, node){
        self.callRemote("saveClicked", $(self.nodeById("editEmployee")).serializeArray()).addCallback(
            function(ret){
                if (ret) {
                   self.addChildWidgetFromWidgetInfo(ret).addCallback(
                        function childAdded(widget){
                            console.log(41);
                            console.log(widget);
                            self.nodeById("employeeOptions").appendChild(widget.node);
                            widget.callback=function(){
                                self.nodeById("employeeOptions").style.display="none";
                            }
                        }
                    );
                }
                else{
                    self.nodeById('employeeOptions').style.display='none';
                }
            }
        )
    },
    function onClose(self, node){
        self.node.parentNode.removeChild(self.node);
    },
    function showCommand(self, node){
        self.callRemote("showCommand", node.value);
    }

);
