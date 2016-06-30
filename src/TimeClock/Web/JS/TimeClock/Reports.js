// import TimeClock.Commands
// import Ace
// import List

"use strict";

var types = {
    int:'number',
    float:'number',
    str:'text'
};

TimeClock.Reports = TimeClock.Commands.subclass("TimeClock.Reports");
TimeClock.Reports.methods(
    function newReport(self, node){
        self.nodeById('newReport').style.display='none';
        self.nodeById('newReportName').style.display='block';
        self.nodeById('newReportDescription').style.display='block';
        self.busyCallRemote("showEditor");
    },
    function getNameAndDescr(self, node){
        self.busyCallRemote('setNameAndDescr', self.nodeById('newReportName').value, self.nodeById('newReportDescription').value);
        self.nodeById('newReportName').style.display='none';
        self.nodeById('newReportDescription').style.display='none';
        self.nodeById('newReportName').value='';
        self.nodeById('newReportDescription').value='';
        self.nodeById('newReport').style.display='block';
    },
    function viewDetails(self, node){
        self.busyCallRemote("viewDetails").addCallback(function(params){
            var newNode = params[0];
            var reportName = params[1];
            var reportDescription = params[2];
            self.nodeById('reportName').value=reportName;
            self.nodeById('reportName').style.display = 'block';
            self.nodeById('reportDescription').value=reportDescription;
            self.nodeById('reportDescription').style.display = 'block';
            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.node.appendChild(widget.node);
                        widget.editorSaveCallback = function(s){
                            self.onSave();
                        }
                    }
                );
        });
    },
    function listReports(self, node){
        self.busyCallRemote('listReports').addCallback(function(newNode){
            self.addChildWidgetFromWidgetInfo(newNode).addCallback(
                    function childAdded(widget){
                        self.node.replaceChild(widget.node, node);

                    }
                );
        });
        self.nodeById('refresh').style.display='block';
    },
    function refreshReports(self, node){
        self.busyCallRemote('listReports').addCallback(function(newNode){
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
    function runReport(self, node){
        var args = [];
        for (var i=0; i<self.lst.items.length;i++){
            args.push(self.lst.items[i].elm.children[1].value);
        }
        self.busyCallRemote("runReport", args).addCallback(function(retval){
            var report, mimetype;
            report = retval[0];
            mimetype = retval[1];
            var blob = new Blob([report], {type: mimetype});
            var url = URL.createObjectURL(blob);
            window.open(url,'_blank');
        });
    },
    function onSave(self){
        self.nodeById('reportName').style.display='none';
        self.nodeById('reportDescription').style.display='none';
        self.busyCallRemote("save", self.nodeById('reportName').value, self.nodeById('reportDescription').value);
    },
    function prepareReport(self, node){
        self.nodeById("openReport").style.display='none';
        self.nodeById("runReport").style.display='block';

        self.busyCallRemote("getArgs").addCallback(function(params) {
            var count = params.length;
            var options = {
                valueNames: [ 'value', 'label'],
                item: '<li><h3 class="label"></h3><input class="value"> </input></li>'
            };
            var args = [];
            for (var idx=0; idx<count;idx++){
                var param = params[idx];
                var type = "text";
                if (param instanceof Array){
                    type = param[1];
                    param = param[0];
                }
                args.push({value: '', label:param, type:type});
            }
            console.log(args);
            self.lst = new List(self.node, options, args);
            self.argCount = count;
            for (var idx=0; idx<count;idx++){
                var i = self.lst.items[idx];
                i.elm.children[1].type = types[i._values.type];
                if (i._values.type=='int'){
                    i.elm.children[1].step = 1;
                }
            }
        });
    }
);
