import logging

from . import global_variables
from . import client_wrapper


def checkQuantity():
    try:
        curr_price = float(client_wrapper.getCurrValue(global_variables.symbol));
        total_price = curr_price * global_variables.quantity;
        logging.info("current price : %f",curr_price);
        
        symbol_balance = client_wrapper.getAssetBalance();
        curr_USDT_balance = float(symbol_balance.loc[symbol_balance['asset']== "USDT" , 'walletBalance'].iloc[0]);
        if(global_variables.symbol == "BTCUSDT"):
            curr_symbol_balance = float(symbol_balance.loc[symbol_balance['asset']== "BTC" , 'walletBalance'].iloc[0]);
        elif(global_variables.symbol == "BNBUSDT"):
            curr_symbol_balance = float(symbol_balance.loc[symbol_balance['asset']== "BNB" , 'walletBalance'].iloc[0]);
        ##elif TODO: Add more symbols
        logging.info("Current USDT Balance : %f",curr_USDT_balance);
        logging.info("Current symbol Balance : %f",curr_symbol_balance);
        
    except (AttributeError, UnboundLocalError) as e:        
        logging.error("Attribution error caught : %s",e);        
    else:
        if(global_variables.side == "BUY"):
            if(curr_USDT_balance > total_price):
                logging.info("Log : Quantity within balance limit %f",curr_USDT_balance);
                return 1;
            else:
                logging.error("LOG: Quantity out of balance limit %f",curr_USDT_balance);
                return -1;
        if(global_variables.side == "SELL"):
            if(curr_symbol_balance >= global_variables.quantity):
                logging.info("Log : Quantity within balance limit %f",curr_symbol_balance);
                return 1;
            else:
                logging.error("LOG: Quantity out of balance limit %f",curr_symbol_balance);
                return -1;
    finally:
        logging.info("Log : checkQuantity() execution completed");
        
    
def checkPriceLimit():
    curr_price = float(client_wrapper.getCurrValue(global_variables.symbol));
    if((global_variables.price > (1.05 * curr_price)) or (global_variables.price < (0.95 * curr_price))):
        logging.error("Log : price out of 5-percent limit of %f",curr_price);
        return -1;
    else:
        logging.info("Log : price within 5-percent limit of %f",curr_price);
        return 1;
        #if(global_variables.side == "SELL"):
        #   return 1;
        #if(global_variables.side == "BUY"):
        #    total_price = curr_price * global_variables.quantity;
        #    USDT_balance = client_wrapper.getAssetBalance();
        #    curr_USDT_balance = float(USDT_balance.loc[USDT_balance['asset']== "USDT" , 'walletBalance'].iloc[0]);
        # 
        #    if(curr_USDT_balance > total_price):
        #        logging.info("Log : Quantity within balance limit %f",curr_USDT_balance);
        #        return 1;
        #    else:
        #        logging.error("LOG: Quantity out of balance limit %f",curr_USDT_balance);
        #        return -1;
        
        
def checkEnvVariables():        
    if(not global_variables.api_key):
        logging.error("Error: API key is not set properly");
        logging.info("Set your API key in .env file");
        exit(1);
        
    if(not global_variables.api_secret):
        logging.error("Error: API secret is not set properly");
        logging.info("Set your API secret in .env file");
        exit(1);
        
    if(not global_variables.testnet_url):
        logging.error("Error: testnet url is not set properly");
        logging.info("Set your testnet url in .env file");
        exit(1);
    
    