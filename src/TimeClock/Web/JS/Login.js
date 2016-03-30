// import Nevow.Athena
// import Divmod.Runtime
// import redirect

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

    }
);
