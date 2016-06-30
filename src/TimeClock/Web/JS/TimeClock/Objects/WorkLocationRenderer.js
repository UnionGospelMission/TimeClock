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

    }



);
