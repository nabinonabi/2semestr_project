$(document).ready(function(){
    
    window.BXReady.Market.buttonUp =  {
                 
        init: function(top_show, delay){           
            
            $(window).scroll(function () {      
                if ($(this).scrollTop() > top_show) $('.bxr-button-up').fadeIn();
                    else $('.bxr-button-up').fadeOut();
                });
                
                $('.bxr-button-up').click(function () {
                    $('body, html').animate({
                        scrollTop: 0
                    }, delay);
                 });         
        },
    };
});