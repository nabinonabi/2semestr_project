$(document).ready(function(){

    window.BXReady.Market.Compare = {

        compareUrl: '/ajax/compare.php',
        messList : '',
        mess : '',
        iblockID : 0,
        scrollUp: false,
        list: '',

        animateShowIndicator: function(element,sClass){
            element.css('opacity', '0').addClass(sClass+'-active').animate({'opacity': '1'}, 1000, "easeOutExpo");
        },

        reload: function(){
//            compare = this;
            compare = window.BXReady.Market.Compare;
            url = compare.ajaxURL+'?ajaxbuy=yes&rg='+Math.random();

            $.ajax({
                url: url,
                success: function(data){
                    compare.refresh(data);
                }
            });
        },

        refresh: function(data){
//            compare = this;
            compare = window.BXReady.Market.Compare;
            $('#bxr-compare-body').html(data);
            $('#bxr-counter-compare').html($('#bxr-counter-compare-new').html());

            compare.list = JSON.parse($('#bxr-compare-jdata').html());

            $('.bxr-indicator-item-compare').data("compare", 0);
            if (compare.list != null && Object.keys(compare.list).length > 0){
                $.each(compare.list, function(index, elem) {
                    $('.bxr-indicator-item-compare[data-item='+index+']').each(function() {
                        if (!$(this).hasClass('bxr-counter-compare-active'))
                            compare.animateShowIndicator($(this),'bxr-counter-compare');
                    });
//                    if (!$('.bxr-indicator-item-compare[data-item='+index+']').hasClass('bxr-counter-compare-active'))
//                        compare.animateShowIndicator($('.bxr-indicator-item-compare[data-item='+index+']'),'bxr-counter-compare');
                    $('.bxr-indicator-item-compare[data-item='+index+']').data("compare", 1);
                });
            }else{
                $('.bxr-indicator-item-compare').removeClass('bxr-counter-compare-active');
            }
            
            $('.bxr-indicator-item-compare').each(function() {
                if ($(this).data('compare') == 0)
                    $(this).removeClass('bxr-counter-compare-active');
            });

            BXReady.Market.Basket.autoSetVertical();


        },

        add: function(itemID){

//            compare = this;
            compare = window.BXReady.Market.Compare;
            if (
                compare.ajaxURL.length <= 0
                    || compare.iblockID <= 0)
                return;

            url = compare.ajaxURL+'?action=ADD_TO_COMPARE_LIST&bid='+compare.iblockID+'&id='+itemID+'&ajaxbuy=yes&rg='+Math.random();

            $.ajax({
                url: url,
                success: function(data){

                    compare.refresh(data);
                }
            });

            return false;
        },

        delete: function(itemID){

//            compare = this;
            compare = window.BXReady.Market.Compare;
            if (
                compare.ajaxURL.length <= 0
                    || compare.iblockID <= 0)
                return;

            url = compare.ajaxURL+'?action=DELETE_FROM_COMPARE_LIST&bid='+compare.iblockID+'&id='+itemID+'&ajaxbuy=yes&rg='+Math.random();

            $.ajax({
                url: url,
                success: function(data){

                    compare.refresh(data);
                    BXReady.closeAjaxShadow('basket-body-shadow');
                }
            });

            return false;
        },

        init: function(){

//            compare = this;
            compare = window.BXReady.Market.Compare;
            compare.reload();

            $(document).on(
                'click',
                '.bxr-compare-button',
                function(){

                    itemID = $(this).data('item');

                    n = 0;

                    if (compare.list == null){

                    }else{
                        value = parseInt(compare.list[itemID]);
                        if (!isNaN(value) && value >0){
                            n = 1;
                        }
                    }



                    if (n == 0){
                        compare.add(itemID);
                    }else{
                        compare.delete(itemID);
                    }

                    return false;
                }
            );

            $(document).on(
                'click',
                '.compare-button-delete',
                function(){

                    itemID = $(this).data('item');

                    BXReady.showAjaxShadow('#bxr-compare-body','basket-body-shadow');
                    compare.delete(itemID);
                    return false;
                }
            );

            /*$(document).on(
                'click',
                '.compare-button-group',
                function(){
                    $('#bxr-compare-body').fadeToggle(200);
                    $('.basket-button-group').hide();

                    return false;
                }
            );*/
        }

    };
    
//    if (typeof BXReady.Market.loader != 'object')
//            BXReady.Market.loader = [];
//    BXReady.Market.loader.push(window.BXReady.Market.Compare.reload);
});