// import TimeClock.Commands
// import List

TimeClock.SubAccounts = TimeClock.Commands.subclass("TimeClock.SubAccounts");
TimeClock.SubAccounts.methods(
    function __init__(self, node){
        TimeClock.SubAccounts.upcall(self, "__init__", node);
        self.table = self.node.getElementsByTagName('table')[0];
        self.valueNames = [];

        if (self.table.tHead.rows.length>1 && self.table.tBodies[0].rows.length > 0) {
            for (var i=0; i< self.table.tHead.rows[1].cells.length; i++){
                self.valueNames.push(self.table.tHead.rows[1].cells[i].innerHTML);
            }
            self.options = {
                valueNames: self.valueNames
            };
            self.lst = new List(self.node, self.options);
        }
        for (var idx=0; idx<node.length; idx++){
            self.itemClicked(self.table.tBodies[0].rows[node[idx]]);
        }
    },
    function onClose(self, node){
        self.node.parentNode.removeChild(self.node);
        if (self.widgetParent){
            self.widgetParent.removeChildWidget(self);
        }
    },
    function replaceSelf(self, node){
        self.node.parentNode.replaceChild(node, self.node);
        if (self.widgetParent){
            self.widgetParent.removeChildWidget(self);
        }

    },
    function toggleActive(self, node){
        self.callRemote("toggleActive", node.dataset.storeid, node.checked);
    }
);
