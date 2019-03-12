const quiz = (function(){

    const button = document.querySelector(".form__submit");
    
    button.addEventListener("click",(e)=>{
    $('#quizModal').modal('show');
    e.preventDefault();
    })
    
})();
    