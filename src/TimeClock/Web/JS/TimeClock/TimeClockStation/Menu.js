// import TimeClock.TimeClockStation
'use strict';

TimeClock.TimeClockStation.Menu = TimeClock.TimeClockStation.subclass("TimeClock.TimeClockStation.Menu");
TimeClock.TimeClockStation.Menu.methods(
    function updateTime(self, hours){
        self.nodeById('currentTime').innerHTML = hours;
    },
    function logout(self, node){
        document.cookie = 'lastPage=login;';
        $.redirectPost("/");
    }
);
