// import TimeClock.Widgets
// import List
// import jquery.ui
// import jquery.tablesorter
"use strict";

// @TODO: finish removing List.selected

TimeClock.Widgets.List = TimeClock.Widgets.subclass("TimeClock.Widgets.List");
TimeClock.Widgets.List.methods(
    function headerClicked(self, node){
        if (self.lst){
            var key=0;
            for (var p=node; p.previousElementSibling!=null; key++){
                p = p.previousElementSibling;
            }
            if (self.lastKey==key){
                if (self.order == 'desc'){
                    self.order = 'asc';
                }
                else{
                    self.order = 'desc';
                }
            }
            else {
                self.order='asc';
            }
            var options = {
                order: self.order,
                sortFunction: function(a, b) {
                    var aval;
                    var bval;
                    var ainp = $(a.elm).find('input');
                    var binp = $(b.elm).find('input');
                    if (key < ainp.length){
                        if (ainp[key].type=='checkbox'){
                            aval = ainp[key].checked;
                        }
                        else {
                            aval = $(ainp[key]).val();
                        }
                    }
                    else{
                        aval = null;
                    }
                    if (key < binp.length){
                        if (binp[key].type=='checkbox'){
                            bval = binp[key].checked;
                        }
                        else {
                            bval = $(binp[key]).val();
                        }
                    }
                    else{
                        bval = null;
                    }
                    return self.lst.utils.naturalSort(aval, bval, options);

                }

            };
            self.lst.sort(node.innerHTML, options);
            self.lastKey = key;
        }
    },
    function __init__(self, node){
        var initNode = document.getElementById('athena-init-args-' + node.id.split(':')[1]);
        if (initNode){
            var initText = initNode.value;
            self.args = eval(initText);
        }
        else{
            self.args = [-1];
        }
        self.toProcess=0;
        TimeClock.Widgets.List.upcall(self, "__init__", node);
        self.limit = parseInt(self.args[0]);
        self.table = self.node.getElementsByTagName('table')[0];
        self.valueNames = [];

        self.searchFunction = function(match, item, val) {
            if (self.isSelected(item)) {
                item.found = true;
                return true;
            }
            match(item);
            if (!item.found) {
                var elm = item.elm;
                var ih = elm.innerHTML;
                if (ih.toLowerCase().indexOf(val) > -1) {
                    item.found = true;
                    return true;
                }
            }
            else {
                return true;
            }
        };

        if (self.table.tHead.rows.length>1 && self.table.tBodies[0].rows.length > 0) {
            for (var i=0; i< self.table.tBodies[0].rows[0].cells.length; i++){
                if (self.table.tBodies[0].rows[0].cells[i].className!=undefined){
                    self.valueNames.push(self.table.tBodies[0].rows[0].cells[i].className);
                }

            }
            self.options = {
                valueNames: self.valueNames,
                searchFunction: self.searchFunction
            };
            self.lst = new List(self.node, self.options);
        }

    },
    function isSelected(self, itm) {
        return itm.elm.style.backgroundColor=='teal' || itm.elm.style.backgroundColor=='green'
    },
    function getSelected(self){
        var o = [];
        var a = self.getAll();
        for (var i in a){
            if (a.hasOwnProperty(i)){
                if (self.isSelected(a[i])){
                    o.push(TimeClock.get(a[i].elm));
                }
            }
        }
        return o;
    },
    function remove(self, idx){
        var n = TimeClock.fromAthenaID(idx);
        self.removeChildWidget(n);
        //self.lst.remove(n.node);
        n.node.parentNode.removeChild(n.node);
        self.lst = new List(self.node, self.options);
    },
    function serverAppend(self, newnode) {
        self.toProcess++;
        if (self.toProcess < 1){
            self.toProcess = 1;
        }
        self.append(newnode);
    },
    function append(self, newnode) {
        self.addChildWidgetFromWidgetInfo(newnode).addCallback(
            function childAdded(newwidget){
                var idx = self.table.tBodies[0].rows.length;
                try {
                    var sb = TimeClock.get(self.table.tBodies[0].rows[idx-1]);
                    if (sb) {
                        if (sb.__class__ == TimeClock.Widgets.SaveList) {
                            idx--;
                        }
                    }
                }
                catch (exc) {

                }

                self.table.tBodies[0].insertBefore(newwidget.node, self.table.tBodies[0].rows[idx]);
                if (--self.toProcess==0 && self.table.tBodies[0].rows.length > 0){
                    self.valueNames = [];
                    for (var i=0; i< self.table.tBodies[0].rows[0].cells.length; i++){
                        if (self.table.tBodies[0].rows[0].cells[i].className!=undefined){
                            self.valueNames.push(self.table.tBodies[0].rows[0].cells[i].className);
                        }

                    }
                    self.options = {
                        valueNames: self.valueNames,
                        searchFunction: self.searchFunction
                    };
                    if (self.lst == undefined) {
                        self.lst = new List(self.node, self.options);
                    }
                    else {
                        self.lst.reIndex();
                    }
                }



            }
        ).addErrback(function(){
            if (--self.toProcess==0) {
                self.valueNames = [];
                for (var i=0; i< self.table.tBodies[0].rows[1].cells.length; i++){
                    if (self.table.tBodies[0].rows[0].cells[i].className!=undefined){
                        self.valueNames.push(self.table.tBodies[0].rows[0].cells[i].className);
                    }

                }
                self.options = {
                    valueNames: self.valueNames,
                    searchFunction: self.searchFunction
                };
                self.lst = new List(self.node, self.options);
            }
            console.log(167);
            console.log(arguments);
            console.log(newnode);
        });
    },
    function select(self, selected, newelements){
        if (newelements){
            var sl;
            while (self.childWidgets.length>0){
                var m = self.childWidgets.pop();
                if (m.__class__==TimeClock.Widgets.SaveList) {
                    sl = m;
                }
                if (self.lst!=undefined){
                    self.lst.remove(m.node);
                }
            }
            if (sl) {
                self.childWidgets.push(sl);
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
        if (!self.lst) {
            return [];
        }
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
