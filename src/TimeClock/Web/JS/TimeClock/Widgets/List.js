// import TimeClock.Widgets
// import List
// import jquery.ui
// import jquery.tablesorter
"use strict";

// @TODO: finish removing List.selected

TimeClock.Widgets.List = TimeClock.Widgets.subclass("TimeClock.Widgets.List");
TimeClock.Widgets.List.methods(
    function __init__(self, node){
        var initNode = document.getElementById('athena-init-args-' + node.id.split(':')[1]);
        if (initNode){
            var initText = initNode.value;
            self.args = eval(initText);
        }
        else{
            self.args = [-1];
        }
        TimeClock.Widgets.List.upcall(self, "__init__", node);
        self.limit = parseInt(self.args[0]);
        self.table = self.node.getElementsByTagName('table')[0];
        self.valueNames = [];

        if (self.table.tHead.rows.length>1 && self.table.tBodies[0].rows.length > 0) {
            for (var i=0; i< self.table.tHead.rows[1].cells.length; i++){
                if (self.table.tBodies[0].rows[0].cells[i].className!=undefined){
                    self.valueNames.push(self.table.tBodies[0].rows[0].cells[i].className);
                }

            }
            self.options = {
                valueNames: self.valueNames
            };
            self.lst = new List(self.node, self.options);
            $(self.table).tablesorter();
        }

    },
    function getSelected(self){
        var o = [];
        var a = self.getAll();
        for (var i in a){
            if (a.hasOwnProperty(i)){
                if (a[i].elm.style.backgroundColor=='teal' || a[i].elm.style.backgroundColor=='green'){
                    o.push(TimeClock.get(a[i].elm));
                }
            }
        }
        return o;
    },
    function remove(self, idx){
        var n = TimeClock.fromAthenaID(idx);
        self.removeChildWidget(n);
        n.node.parentNode.removeChild(n.node);
    },
    function append(self, newnode){
        self.addChildWidgetFromWidgetInfo(newnode).addCallback(
            function childAdded(newwidget){
                self.table.tBodies[0].appendChild(newwidget.node);
                if (--self.toProcess==0){
                    self.valueNames = [];
                    for (var i=0; i< self.table.tHead.rows[1].cells.length; i++){
                        if (self.table.tBodies[0].rows[0].cells[i].className!=undefined){
                            self.valueNames.push(self.table.tBodies[0].rows[0].cells[i].className);
                        }

                    }
                    self.options = {
                        valueNames: self.valueNames
                    };
                    self.lst = new List(self.node, self.options);
                    $(self.table).tablesorter({
                        textExtraction: function(n) {
                            var inp = n.getElementsByTagName('input');
                            if (inp.length){
                                if (inp[0].type=='checkbox'){
                                    return inp[0].checked ? "checked" : '';
                                }
                                return inp[0].value;
                            }
                            return '';
                        }
                    });
                }
            }
        );
    },
    function select(self, selected, newelements){
        if (newelements){
            console.log(52);
            console.log(newelements);
            console.log(54, selected);
            while (self.childWidgets.length>0){
                var m = self.childWidgets.pop();
                if (self.lst!=undefined){
                    self.lst.remove(m.node);
                }
            }
            self.toProcess = selected.length;
            for (var indx=0; indx<selected.length;indx++){
                var newnode = selected[indx];
                self.append(newnode);
            }
            return;
        }
        var oldSelected = self.getAll();
        while (oldSelected.length > 0){
            var s = oldSelected.pop();
            s.elm.style.backgroundColor = "white";
        }
        for (var idx=0;idx<selected.length;idx++){
            var n = TimeClock.fromAthenaID(selected[idx]);
            n.node.style.backgroundColor = "teal";
        }
    },
    function getAll(self){
        return self.lst.filter(function(x){
            return x.elm.tagName == 'TR';
        });
    },
    function itemClicked(self, node, evt){
        var e = window.event || evt;
        if (e){
            var widget = TimeClock.get(e.target);
        }
        else{
            var widget = TimeClock.get(node);
        }
        return self.doItemClicked(widget);
    },
    function doItemClicked(self, widget){
        if (self.node.dataset.selectable!="True"){
            return true;
        }
        var selected = self.getSelected();
        if (selected.indexOf(widget)+1){
            selected.remove(widget);
            widget.node.style.backgroundColor=self.getColor(widget.node.style.backgroundColor);
        }
        else{
            if (self.limit==-1 || self.limit>selected.length){
                selected.push(widget);
                widget.node.style.backgroundColor=self.getColor(widget.node.style.backgroundColor);
            }
            else if (self.limit==1){
                selected[0].node.style.backgroundColor = self.getColor(selected[0].node.style.backgroundColor);
                widget.node.style.backgroundColor = self.getColor(widget.node.style.backgroundColor);
            }


        }
    },
    function getColor(self, color){
        var nc = null;
        switch (color){
            case 'teal':
                nc = 'blue';
                break;
            case 'white':
            case '':
                nc = 'green';
                break;
            case 'blue':
                nc = 'teal';
                break;
            case 'green':
                nc = 'white';
                break;
        }
        return nc;
    },
    function reset(self){
        var selected = self.getAll();
        for (var idx=0; idx< selected.length; idx++){
            var nc = null;
            if (!selected[idx].elm){
                continue;
            }
            switch (selected[idx].elm.style.backgroundColor){
                case 'blue':
                case 'teal':
                    nc = 'teal';
                    break;
                case 'green':
                case 'white':
                    nc = 'white';
                    break;
            }
            selected[idx].elm.style.backgroundColor = nc;
        }
    },
    //function itemDblClicked(self, node) {
    //    if (self.noclick){
    //        return;
    //    }
    //    self.noclick = true;
    //    self.busyCallRemote("itemDblClicked", node.children[0].dataset.index).addCallback(
    //        function (newNode) {
    //            self.noclick = false;
    //            if (!newNode) {
    //                return;
    //            }
    //            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
    //                function childAdded(widget) {
    //                    self.node.appendChild(widget.node);
    //                }
    //            );
    //        }
    //    );
    //},
    function onClose(self, node){
        self.node.parentNode.removeChild(self.node);
        if (self.widgetParent){
            self.widgetParent.removeChildWidget(self);
        }
    },
    function replaceSelf(self, node) {
        self.node.parentNode.replaceChild(node, self.node);
        if (self.widgetParent) {
            self.widgetParent.removeChildWidget(self);
        }
    }
    //},
    //function callParent(self, node){
    //    console.log(52);
    //    var result = Nevow.Athena.Widget.dispatchEvent(
    //        self.widgetParent, "onclick", node.dataset.parentFunction,
    //        function() {
    //            return method.call(widget, node);
    //        });
    //    console.log(result);
    //    return result;
    //}
);
