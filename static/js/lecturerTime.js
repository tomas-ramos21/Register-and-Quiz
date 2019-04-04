// github link for timer function https://github.com/husa/timer.js/ for vendor functions like .start() , .stop() details

(function(){
    const lecturerTime = new Timer();
    var countDownTime = 5 * 60; // 5 minutes , timer set for lectuer
    var countDownMins = countDownTime/60; // the timer in mins
    
    // changes the text conntent of h1 to be time in minutes 
    document.querySelector(".timer-display").textContent = countDownMins;
    
    

    // starts the countdown timer and on end shows a message on the browser that time is up
    lecturerTime.start(countDownTime).on("end",()=>{
        alert("Time is up");
    })


    // if the lecturer clicks the stop button
    document.querySelector(".stop").addEventListener("click",()=>{
        lecturerTime.stop(); // stops the timer
        alert("timer has stopped");
    })

})(); // immediately invoke function expression


