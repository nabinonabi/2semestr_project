if (window){
    window.catalogEcommerceV2Lite = {
        resizeVerticalBlock: function(){
            var $maxHeight = [];
            var $maxNameHeight = [];

            // resize names

            $('.bxr-ecommerce-v2-lite[data-resize=1]').each(function(){

                uid = $(this).data('uid');
                $nameContainer = $(this).children('.bxr-element-container').children('.bxr-element-name');

                if (!(uid in $maxNameHeight)) {
                    $maxNameHeight[uid] = 0;
                }

                if ($nameContainer.height() > $maxNameHeight[uid]) $maxNameHeight[uid] = $nameContainer.height();

            });

            $('.bxr-ecommerce-v2-lite[data-resize=1]').each(function(){

                uid = $(this).data('uid');
                $nameContainer = $(this).children('.bxr-element-container').children('.bxr-element-name');

                if ($nameContainer.height() <= $maxNameHeight[uid]) {
                    $nameContainer.height($maxNameHeight[uid]);
                }

            });

            // resize container

            $('.bxr-ecommerce-v2-lite[data-resize=1]').each(function(){

                uid = $(this).data('uid');
                if (!(uid in $maxHeight)) {
                    $maxHeight[uid] = 0;
                }
                if ($(this).height()>$maxHeight[uid]) $maxHeight[uid] = $(this).height();
            });

            $('.bxr-ecommerce-v2-lite[data-resize=1]').each(function(){

                uid = $(this).data('uid');
                if ($(this).height() <= $maxHeight[uid]) {
                    $(this).children('.bxr-element-container').height($maxHeight[uid]);
                    $(this).height($maxHeight[uid]);
                }
            });
        }
    }

    $(document).ready(function(){

        catalogEcommerceV2Lite.resizeVerticalBlock();

    });
    
    if (typeof BXReady.Market.loader != 'object')
            BXReady.Market.loader = [];
    BXReady.Market.loader.push(catalogEcommerceV2Lite.resizeVerticalBlock);

    $(window).resize(function(){
        catalogEcommerceV2Lite.resizeVerticalBlock();
    });
    
    var current_offer_id;
    var trade_id;
    var trade_name;
    var trade_link;
    var formRequestMsg;
    
    $(document).on("mouseover", ".bxr-ecommerce-v2-lite .bxr-trade-request", function() {
        current_offer_id = $(this).data('offer-id');
        trade_id = $(this).data('trade-id');
        trade_name = $(this).data('trade-name');
        trade_link = $(this).data('trade-link');
        
        strParams = "";
        $(this).closest('.bxr-ecommerce-v2-lite').find('li.bx_active').each(function() {
            strParams += $(this).data('prop-name')+': '+$(this).attr('title')+', ';
        });
        strParams = strParams.slice(0,-2);
        
        formRequestMsg = $(this).data('msg').replace("#PARAMS#",strParams);
    });

}

