// import TimeClock.Objects
// import jquery
// import Ace
// import Ace.mode_python
// import Ace.theme_twilight

"use strict";


TimeClock.Objects.DynamicReportRenderer = TimeClock.Objects.subclass("TimeClock.Objects.DynamicReportRenderer");
TimeClock.Objects.DynamicReportRenderer.methods(
    function __init__(self, node){
        self.options = {
            timeFormat: 'HH:mm:ss z',
            dateFormat: 'yy-mm-dd',
            showTimezone: true,
            timezone: 'AUTO',
            timezoneList: [
                { value: "AUTO",  label: 'AUTO' },
                { value: 'PDT', label: 'PDT'},
                { value: 'PST',  label: 'PST' }
            ]
        };
        TimeClock.Objects.DynamicReportRenderer.upcall(self, "__init__", node);
        self.editor = ace.edit(self.nodeById('editor'));
        //self.editor.setValue(val);
        ace.config.set("basePath", "/jsmodule/Ace");
        self.editor.setTheme("ace/theme/twilight");
        self.editor.getSession().setMode("ace/mode/python");
        self.editor.on("change", function(e){
            if (!self.suppress){
                self.callRemote('editorChanged', self.editor.getValue());
            }
        });
        $('.IDateTime', self.node).datetimepicker(self.options);
        $(self.node).keypress(function(event) {
            if (!(event.which == 115 && event.ctrlKey) && !(event.which == 19)) return true;
            self.saveClicked(null, event);
            return false;
        });
    },

    function newValues(self, args){
        TimeClock.Objects.DynamicReportRenderer.upcall(self, 'newValues', args);
        if (args.code != undefined) {
            if (self.editor.getValue()!=args.code){
                self.suppress = true;
                var cpos = self.editor.getCursorPosition();
                var focused = self.editor.isFocused();
                self.editor.setValue(args.code);
                self.editor.gotoLine(cpos.row + 1, cpos.column);
                if (focused) {
                    self.editor.focus();
                }
                self.suppress = false;
            }
        }
        if (args.args!=undefined){
            self.nodeById('arguments').innerHTML = args.args;
            $('.IDateTime', self.node).datetimepicker(self.options);
        }
    },
    function runReport(self, node, evt) {
        var args = [];
        var e = self.nodeById('arguments').getElementsByTagName('input');
        for (var idx=0; idx< e.length;idx++){
            var ele = e[idx];
            if (ele.id!=''){
                if (ele.type!='checkbox'){
                    args.push(ele.value);
                }
                else{
                    args.push(ele.checked);
                }
            }
        }

        self.busyCallRemote("runReport", self.nodeById('format').value, args).addCallback(function(retval){
            console.log(retval);
            var report, mimetype;
            report = retval[0];
            mimetype = retval[1];
            if (mimetype=='livefragment'){
                console.log(63, report);
                self.addChildWidgetFromWidgetInfo(report).addCallback(
                    function childAdded(newwidget) {
                        console.log(65, newwidget);
                        $(newwidget.node).dialog({close: newwidget.onClose});
                    }
                );
            }
            else {
                var blob = new Blob([report], {type: mimetype});
                var url = URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.style = "display: none";
                document.body.appendChild(a);
                a.href = url;
                a.download = self.nodeById('name').value + "." + self.nodeById('format').value;
                a.target = '_blank';
                a.click();
                //window.open(url,'_blank');
                document.body.removeChild(a);
            }

        });
    },
    function saveClicked(self, node, evt){
        console.log(89);
        var event = window.event || evt;
        if (event!=undefined){
            event.stopPropagation();
        }
        console.log(94);
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
        vars['code'] = self.editor.getValue();
        console.log(vars);
        self.busyCallRemote('saveClicked', vars).addCallback(function(){
            if (self.expanded) {
                self.expand(null);
            }
        });

    }



);
