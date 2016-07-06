// import TimeClock

"use strict";


TimeClock.Objects = TimeClock.subclass("TimeClock.Objects");
TimeClock.Objects.methods(
    function __init__(self, node){
        TimeClock.Objects.upcall(self, "__init__", node);
        self.expanded = false;
    },
    function expand(self, node){
        self.expanded = !self.expanded;
        if (self.expanded){
            self.nodeById('expand-button').style.display='none';
            self.nodeById('unexpand-button').style.display='block';
            self.nodeById('expanded').style.display='block';
        }else{
            self.nodeById('expand-button').style.display='block';
            self.nodeById('unexpand-button').style.display='none';
            self.nodeById('expanded').style.display='none';
        }
    },
    function newValues(self, args){
        for (var key in args){
            if (args.hasOwnProperty(key)){
                try{
                    var inp = self.nodeById(key);
                }
                catch (e){
                    continue;
                }
                if (inp.type=='checkbox'){
                    inp.checked = args[key];
                }
                else{
                    inp.value = args[key];
                }
            }
        }
    },
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
        e = self.node.getElementsByTagName('select');
        for (var idx=0; idx< e.length;idx++){
            var ele = e[idx];
            if (ele.id!=''){
                vars[ele.id.split('-')[1]] = ele.value;
            }
        }
        console.log(vars);

        self.busyCallRemote('saveClicked', vars);

    }
);
