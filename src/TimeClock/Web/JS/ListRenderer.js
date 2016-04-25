// import TimeClock.Commands
// import List

TimeClock.ListRenderer = TimeClock.Commands.subclass("TimeClock.ListRenderer");
TimeClock.ListRenderer.methods(
    function __init__(self, node){
        var initNode = document.getElementById('athena-init-args-' + node.id.split(':')[1]);
        if (initNode){
            var initText = initNode.value;
            self.args = eval(initText);
        }
        else{
            self.args = [-1];
        }

        TimeClock.ListRenderer.upcall(self, "__init__", node);
        self.limit = parseInt(self.args[0]);
        self.selected = [];
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
    function select(self, selected){
        while (self.selected.length > 0){
            self.itemClicked(self.selected[0]);
        }
        for (var idx=0; idx<selected.length; idx++){
            self.itemClicked(self.table.tBodies[0].rows[selected[idx]]);
        }
    },
    function itemClicked(self, node){
        if (self.node.dataset.selectable!="true"){
            return true;
        }
        if (self.selected.indexOf(node)+1){
            self.selected.pop(node);
            node.style.backgroundColor="white";
        }
        else{
            if (self.limit==-1) {
                self.selected.push(node);
                node.style.backgroundColor = "teal";
            }
            else if (self.limit==1){
                if (self.selected.length==1){
                    self.selected[0].style.backgroundColor = 'white';
                    self.selected.pop(0);

                }
            }

            if (self.limit>self.selected.length){
                self.selected.push(node);
                node.style.backgroundColor = "teal";
            }
        }
    },
    function itemDblClicked(self, node) {
        if (self.noclick){
            return;
        }
        self.noclick = true;
        self.callRemote("itemDblClicked", node.children[0].dataset.index).addCallback(
            function (newNode) {
                self.noclick = false;
                if (!newNode) {
                    return;
                }
                self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget) {
                        self.node.appendChild(widget.node);
                    }
                );
            }
        );
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
    function callParent(self, node){
        console.log(52);
        result = Nevow.Athena.Widget.dispatchEvent(
            self.widgetParent, "onclick", node.dataset.parentFunction,
            function() {
                return method.call(widget, node);
            });
        console.log(result);
        return result;
    }
);
