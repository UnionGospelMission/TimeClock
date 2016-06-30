
TimeClock.ActionPane = TimeClock.subclass("TimeClock.ActionPane");
TimeClock.ActionPane.methods(
    function __init__(self, node) {
        TimeClock.ActionPane.upcall(self, "__init__", node);
        self.commands = {};
        self.currentCommand = null;
    },
    function show(self, name){
        console.log(name);
        console.log(self.commands);
        for (var c in self.commands){
            if (self.commands.hasOwnProperty(c)){
                self.commands[c].hide();
            }
        }
        self.currentCommand = self.commands[name];
        self.currentCommand.show();
    }
);
