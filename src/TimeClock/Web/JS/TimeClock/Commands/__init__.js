// import Nevow.Athena
// import Divmod.Runtime
// import redirect
// import TimeClock

"use strict";
TimeClock.Commands = TimeClock.subclass("TimeClock.Commands");
TimeClock.Commands.methods(
    function __init__(self, node){
        TimeClock.Commands.upcall(self, "__init__", node);
        if (self.node.dataset.toplevel){
            TimeClock.ActionPane.fromAthenaID(2).commands[self.node.dataset.name] = self;
        }
        if (node.style.display!='none' && node.dataset.name){
            TimeClock.ActionPane.fromAthenaID(2).currentCommand = self;
        }
        var doptions = {
            dialogClass: "scroll-y",
            closeOnEscape: false,
            position: { my: "left top", at: "center top", of: window, collision: "none"},
            width: 'auto'

        };
        self.doptions = doptions;
        doptions.beforeClose = function beforeClose( event, ui ) {
            self.hide();
            return false;
        };
        doptions.dragStop = function dragStop(event, ui) {
            var cookie = 'widget_{name}=({x},{y}); Max-Age=2592000;'.format({
                name: self.node.dataset.name,
                x: ui.position.left,
                y: ui.position.top
            });
            document.cookie = cookie;
        };



        setTimeout(function(){
            if (!self.node.dataset.toplevel){
                return;
            }
            var position = window.getCookie('widget_' + self.node.dataset.name);
            if (position) {
                var x, y;
                x = position.split(',')[0].split('(')[1];
                y = position.split(',')[1].split(')')[0];
                doptions.position.my = 'left+{x} top+{y}'.format({x: x, y: y});
                doptions.position.at = 'left top';
            }
            doptions.title = self.node.dataset.title.split('- ')[1];
            self.node.title = doptions.title;
            var wp = self.widgetParent;
            var l1 = self;
            var d1 = $(l1.node).dialog(doptions).parent()[0];
            self.d1 = d1;
            document.body.removeChild(d1);
            wp.node.appendChild(d1);
            self.hide();
        }, 100);
    },
    function runCommand(self, node){
        var args = self.getArgs(node);
        var b = self.setBusy();
        self.busyCallRemote('runCommand', args).addCallback(b);

        return false;
    },
    function getArgs(self, node){
        return $(node).serializeArray();
    },
    function show(self, node){
        TimeClock.Commands.upcall(self, "show", node);
        self.busyCallRemote("load");
    }


);


