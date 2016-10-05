// import TimeClock.Commands
// import jquery.ui

"use strict";
TimeClock.Commands.SetPassword = TimeClock.Commands.subclass("TimeClock.Commands.SetPassword");
TimeClock.Commands.SetPassword.methods(
    function __init__(self, node){
        TimeClock.Commands.SetPassword.upcall(self, '__init__', node);
        self.expired = self.nodesByAttribute('name', 'expired');
        if (self.expired.length > 0) {
            setTimeout(function() {
                self.show();
            }, 500);
        }
    },
    function setPassword(self, node) {
        try {
            var oldpw = self.nodeById('currentPassword').value;
        }
        catch (e) {
            var oldpw = null;
        }
        self.busyCallRemote('setPassword', oldpw, self.nodeById('newPassword').value, self.nodeById('newPasswordAgain').value);

    },
    function logout(self){
        var d = $('<div>Please login again with your new password</div>').dialog({
                buttons: [{
                    text: "OK",
                    click: function() {
                        $.redirectPost('/');
                    }
                }]
            }
        );
    }
);


