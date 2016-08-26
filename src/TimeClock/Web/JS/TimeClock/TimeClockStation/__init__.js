// import TimeClock

TimeClock.TimeClockStation = TimeClock.subclass("TimeClock.TimeClockStation");
TimeClock.TimeClockStation.methods(
    function __init__(self, node){
        TimeClock.TimeClockStation.upcall(self, '__init__', node);
        document.cookie = 'lastPage=tcs;';
    }
);
