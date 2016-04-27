// import Nevow.Athena
// import Divmod.Runtime
// import redirect

TimeClock.MenuPane = Nevow.Athena.Widget.subclass("TimeClock.MenuPane");
TimeClock.MenuPane.methods(
    function __init__(self, node) {
        TimeClock.MenuPane.upcall(self, "__init__", node);
        self.commands = TimeClock.ActionPane.fromAthenaID(2);

    },
    function menuClicked(self, node){
        var name = node.id.split("-")[1];
        self.callRemote('navigate', name);
        self.commands.show(name);
    },
    function hideClockIn(self){
        self.nodeById("clockIn").style.display='none';
        self.nodeById("clockOut").style.display='block';
    },
    function hideClockOut(self){
        self.nodeById("clockOut").style.display='none';
        var nbi = self.nodeById("clockIn");
        if (nbi){
            nbi.style.display='block';
        }
    },
    function updateTime(self, hours){
        self.nodeById('hoursWorked').innerHTML = hours;
    },
    function logout(self, node){
        $.redirectPost("/");
    }

);


TimeClock.ActionPane = Nevow.Athena.Widget.subclass("TimeClock.ActionPane");
TimeClock.ActionPane.methods(
    function __init__(self, node) {
        TimeClock.ActionPane.upcall(self, "__init__", node);
        self.commands = {};
        self.currentCommand = null;
    },
    function show(self, name){
        console.log(name);
        console.log(self.commands);
        if (self.currentCommand){
            self.currentCommand.hide();
        }
        self.currentCommand = self.commands[name];
        self.currentCommand.show();
    }
);
