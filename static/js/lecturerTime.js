// github link for timer function https://github.com/husa/timer.js/ for vendor functions like .start() , .stop() details

(function(){
    let duration = parseInt(document.querySelector(".timer-time").textContent);

    const lecturerTime = new Timer({
        tick:1,
        ontick  : function() {}
    });

    // starts the countdown timer and on end shows a message on the browser that time is up
   const countStart =  lecturerTime.start(duration);


    countStart.options({
         ontick:function(){
            duration --;
            let minutes = Math.trunc(duration / 60);
            let seconds = duration % 60;

            minutes = minutes < 10 ? `0${minutes}` : minutes;
            seconds = seconds < 10 ? `0${seconds}` : seconds;

            document.querySelector(".timer-display").textContent = `Time left ${minutes}: ${seconds}`;


         },
         onend:function(){
            document.querySelector(".timer-display").textContent = `Time is up! 00:00`;
         }
    })

    // event listener for stopping the timer

    document.querySelector(".stop").addEventListener("click",()=>{
        lecturerTime.stop(); // stops the timer
        document.querySelector(".timer-display").textContent = `Timer stopped`;

    })

})(); // immediately invoke function expression
