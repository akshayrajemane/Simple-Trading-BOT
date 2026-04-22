import logging

from . import global_variables
from . import client_wrapper
from . import validators


def placeOrder():
    output = None;
    check_quantity = 0;
    check_price_limit = 0;
    
    if(global_variables.order_type == "MARKET"):
        check_quantity = validators.checkQuantity();
        if( check_quantity == 1 and global_variables.side == "BUY"):
            output = client_wrapper.buyMarketOrder(global_variables.symbol,global_variables.quantity);
        
        if(check_quantity == 1 and global_variables.side == "SELL"):
            output = client_wrapper.sellMarketOrder(global_variables.symbol,global_variables.quantity);
    
    
    if(global_variables.order_type == "LIMIT"):
        check_price_limit = validators.checkPriceLimit();
        if(check_price_limit == 1 and global_variables.side == "BUY"):
            output = client_wrapper.buyLimitOrder(global_variables.symbol,global_variables.quantity,global_variables.price);
        
        if(check_price_limit == 1 and global_variables.side == "SELL"):
            output = client_wrapper.sellLimitOrder(global_variables.symbol,global_variables.quantity,global_variables.price);

    if(output):
        return output;
    else:
        return None;
    
   

    
    
