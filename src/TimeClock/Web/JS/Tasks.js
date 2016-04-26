// import TimeClock.Commands
// import Ace
// import List

TimeClock.Tasks = TimeClock.Commands.subclass("TimeClock.Tasks");
TimeClock.Tasks.methods(
    function newTask(self, node){
        self.nodeById('newTask').style.display='none';
        self.nodeById('newTaskName').style.display='block';
        self.nodeById('newTaskHours').style.display='block';
        self.callRemote("showEditor");
        self.childWidgets[0].onClose=function(node1){
            self.childWidgets[0].hide();
        };
    },
    function getNameAndHours(self, node){
        self.callRemote('setNameAndHours', self.nodeById('newTaskName').value, self.nodeById('newTaskHours').value);
        self.nodeById('newTaskName').style.display='none';
        self.nodeById('newTaskHours').style.display='none';
        self.nodeById('newTaskName').value='';
        self.nodeById('newTaskHours').value='';
        self.nodeById('newTask').style.display='block';
    },
    function listTasks(self, node){
        self.callRemote('listTasks').addCallback(function(newNode){
            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.node.replaceChild(widget.node, node);

                    }
                );
        });
        self.nodeById('refresh').style.display='block';
    },
    function refreshTasks(self, node){
        self.busyCallRemote('listTasks').addCallback(function(newNode){
            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                function childAdded(widget){
                    if (self.childWidgets.length>1){
                        self.childWidgets[0].replaceSelf(widget.node);
                    }
                    else{
                        self.node.appendChild(widget.node);
                    }

                }
            );
        });
    },
    function onSave(self){
        self.nodeById('taskName').style.display='none';
        self.nodeById('taskHours').style.display='none';
        self.busyCallRemote("save", self.nodeById('taskName').value, self.nodeById('taskHours').value);
    },
    function viewDetails(self, node){
        self.busyCallRemote("viewDetails").addCallback(function(params){
            var newNode = params[0];
            var taskName = params[1];
            var taskHours = params[2];
            self.nodeById('taskName').value=taskName;
            self.nodeById('taskName').style.display = 'block';
            self.nodeById('taskHours').value=taskHours;
            self.nodeById('taskHours').style.display = 'block';
            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.node.appendChild(widget.node);
                        widget.editorSaveCallback = function(s){
                            self.onSave();
                        }
                    }
                );
        });
    }

);
