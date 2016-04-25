// import Ace
// import TimeClock.Commands

"use strict";

ace.config.set("basePath", "jsmodule/");


TimeClock.Editor = TimeClock.Commands.subclass("TimeClock.Editor");
TimeClock.Editor.methods(
    function __init__(self, node){
        TimeClock.Editor.upcall(self, "__init__", node);
        self.callRemote('revert').addCallback(function(val){
            self.editor = ace.edit(self.nodeById('editor'));
            self.editor.getSession().setMode("ace/mode/python");
            self.editor.setValue(val);
            self.editor.setTheme("ace/theme/twilight");
        })
    },
    function save(self, node){
        self.callRemote("save", self.editor.getValue());
        var ps = self.editorSaveCallback;
        if (ps){
            ps();
        }
        self.onClose(node);
    },
    function cancel(self, node){
        self.onClose(node);
    }
);
