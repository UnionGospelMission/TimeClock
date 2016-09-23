// import TimeClock.Commands

"use strict";
TimeClock.Commands.SetPassword = TimeClock.Commands.subclass("TimeClock.Commands.SetPassword");
TimeClock.Commands.SetPassword.methods(
    function __init__(self, node){
        TimeClock.Commands.SetPassword.upcall(self, '__init__', node);
    },
    function setPassword(self, node) {
        try {
            var oldpw = self.nodeById('currentPassword').value;
        }
        catch (e) {
            var oldpw = null;
        }
        self.busyCallRemote('setPassword', oldpw, self.nodeById('newPassword').value, self.nodeById('newPasswordAgain').value);

    }
);


