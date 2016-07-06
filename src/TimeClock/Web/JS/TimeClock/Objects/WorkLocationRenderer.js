// import TimeClock.Objects
// import jquery


"use strict";


TimeClock.Objects.WorkLocationRenderer = TimeClock.Objects.subclass("TimeClock.Objects.WorkLocationRenderer");
TimeClock.Objects.WorkLocationRenderer.methods(
    function saveClicked(self, node, event){
        if (event!=undefined){
            event.stopPropagation();
        }

        var vars = {};
        var e = self.node.getElementsByTagName('input');
        for (var idx=0; idx< e.length;idx++){
            var ele = e[idx];
            if (ele.id!=''){
                if (ele.type!='checkbox'){
                    vars[ele.id.split('-')[1]] = ele.value;
                }
                else{
                    vars[ele.id.split('-')[1]] = ele.checked;
                }
            }
        }
        console.log(vars);
        self.busyCallRemote('saveClicked', vars);

    },
    function expand(self, node){
        var expanded=self.expanded;
        if (expanded){
            self.nodeById('expand-button').style.display='block';
            self.nodeById('unexpand-button').style.display='none';
            self.busyCallRemote('unexpand');
            self.expanded.node.parentNode.parentNode.removeChild(self.expanded.node.parentNode);
            self.removeChildWidget(self.expanded);
            self.expanded=null;
        }
        else{
            self.nodeById('expand-button').style.display='none';
            self.nodeById('unexpand-button').style.display='block';
            self.busyCallRemote('expand').addCallback(function (newnode) {
                self.addChildWidgetFromWidgetInfo(newnode).addCallback(function (widget){
                    var td = document.createElement('td');
                    td.appendChild(widget.node);
                    self.node.appendChild(td);
                    self.expanded = widget;
                });
            });
        }
    }



);
