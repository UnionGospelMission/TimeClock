// import Nevow.Athena
// import Divmod.Runtime
// import redirect

LoginPage.ClockedIn = Nevow.Athena.Widget.subclass("LoginPage.ClockedIn");
LoginPage.ClockedIn.methods(
    function clockedIn(self, eid, name) {
        var elist = self.nodeById('employeeList');
        var tr = document.createElement('tr');
        var td1 = document.createElement('td');
        var td2 = document.createElement('td');
        td1.innerHTML = eid;
        td2.innerHTML = name;
        tr.appendChild(td1);
        tr.appendChild(td2);
        elist.appendChild(tr);
    },
    function clockedOut(self, eid, name) {
        var elist = self.nodeById('employeeList');
        for (var i=0; i< elist.rows.length; i++) {
            var row = elist.rows[i];
            if (row.cells[0].innerHTML == eid) {
                elist.removeChild(row);
                i--;
            }
        }
    }
);
LoginPage.Login = Nevow.Athena.Widget.subclass("LoginPage.Login");
LoginPage.Login.methods(
    /**
     * Handle click events on any of the calculator buttons.
     */
    function buttonClicked(self, node) {
        self.callRemote("validate", self.nodeById("username").value, self.nodeById("password").value).addCallback(function(pageId){
            if (pageId=="access denied"){
                alert("Invalid username or password");
            }
            else{
                $.redirectPost("/", {pageId: pageId});
            }

        });
        return false;

    },
    function clockIn(self, node){
        var un = self.nodeById("username");
        var pw = self.nodeById("password");
        self.callRemote("quickValidate", 'clockIn', un.value, pw.value).addCallback(function(success){
            if (success=='access granted'){
                alert("Clocked In");
                un.value = '';
                pw.value = '';
            }
            else{
                alert(success);
            }
        });
    },
    function clockOut(self, node){
        var un = self.nodeById("username");
        var pw = self.nodeById("password");
        self.callRemote("quickValidate", 'clockOut', un.value, pw.value).addCallback(function(success){
            if (success=='access granted'){
                alert("Clocked Out");
                un.value = '';
                pw.value = '';
            }
            else{
                alert(success);
            }
        });
    }
);
