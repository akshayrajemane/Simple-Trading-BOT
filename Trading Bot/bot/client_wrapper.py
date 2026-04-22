import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from dotenv import load_dotenv
import os

from . import global_variables

load_dotenv();

#import few more required classes


pd.set_option('display.max_rows', None);
pd.set_option('display.max_columns', None);
pd.set_option('display.max_colwidth', None);

def getEnvVariables():        
    global_variables.api_key = os.getenv("API_KEY_2");
    global_variables.api_secret = os.getenv("API_SECRET_2");
    global_variables.testnet_url = os.getenv("BINANCE_TESTNET_FUTURES_URL");
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
    

def createClient(api_key, api_secret, testnet_url, test_net):  
    try:
        global_variables.client = Client(api_key,api_secret,testnet=test_net,verbose=True);
        global_variables.client.API_URL = testnet_url + '/fapi';
    except BinanceAPIException as e:
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
        logging.info("API_KEY = %s", api_key);
        logging.info("API_SECRET = %s ", api_secret);
        logging.info("TESTNET_URL = %s", testnet_url);
    else:
        return global_variables.client;
    finally:
        logging.info("Log : createClient() execution completed");
    
    
    
######################### Value and Direction functions ################################
def getAssetBalance():
    try:
        x = global_variables.client.futures_account();
        df = pd.DataFrame(x['assets']);
        # Add or remove columns as required
        df = df[['asset','walletBalance','unrealizedProfit','marginBalance','maxWithdrawAmount','availableBalance','marginAvailable','updateTime']];
    except (BinanceAPIException, AttributeError) as e:
        logging.error("Status: %s",e.status_code);
        logging.error("Error code: %s",e.code);
        logging.error("Message: %s",e.message);
    else:
        return(df);
    finally:
        logging.info("Log : getAssetBalance() execution completed");
    

def getCurrValue(symbol):
    try:
        price = global_variables.client.get_symbol_ticker(symbol=symbol);
    except BinanceAPIException as e:
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        return price['price'];
    finally:
        logging.info("Log : getCurrValue() execution completed");
        

def getDirection(symbol):
    try:
        x = global_variables.client.futures_position_information(symbol=symbol);
    except BinanceAPIException as e:
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        df = pd.DataFrame(x);
        if float(df["positionAmt"].sum()) > 0:
            return "LONG";
        elif float(df["positionAmt"].sum()) < 0:
            return "SHORT";
        else:
            return "FLAT";
    finally:
        logging.info("Log : getDirection() execution completed");
        
   
########################################################################################



################################ Order place/close functions ###########################

def buyLimitOrder(symbol,volume,price):
    try:
        printOrderRequestSummary(symbol,volume,price);
        output = global_variables.client.futures_create_order(
            symbol     = symbol,
            side       = Client.SIDE_BUY,
            type       = Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce= Client.TIME_IN_FORCE_GTC,
            quantity   = volume,
            price      = price,
        )
    except BinanceAPIException as e:
        print("FAIL : Order failed");
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        #printOrderResponseStatus(output);
        #printOrderResponseDetails(output);
        return output;
    finally:
        logging.info("Log : buyLimit() execution completed");


def sellLimitOrder(symbol,volume,price):
    try:
        printOrderRequestSummary(symbol,volume,price);
        output = global_variables.client.futures_create_order(
            symbol     = symbol,
            side       = Client.SIDE_SELL,
            type       = Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce= Client.TIME_IN_FORCE_GTC,
            quantity   = volume,
            price      = price,
        )    
    except BinanceAPIException as e:
        print("FAIL : Order failed");
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);        
    else:
        #printOrderResponseStatus(output);
        #printOrderResponseDetails(output);
        return output;
    finally:
        logging.info("Log : sellLimitOrder() execution completed");


def buyMarketOrder(symbol,quantity):
    try:
        printOrderRequestSummary(symbol,quantity);
        output = global_variables.client.futures_create_order(
            symbol   = symbol,
            side     = Client.SIDE_BUY,
            type     = Client.FUTURE_ORDER_TYPE_MARKET,
            quantity = quantity
        )
    except BinanceAPIException as e:
        print("FAIL : Order failed");
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        #printOrderResponseStatus(output);
        #printOrderResponseDetails(output);
        return output;
    finally:
        logging.info("Log : buyMarketOrder() execution completed");


def sellMarketOrder(symbol,quantity):        
    try:
        printOrderRequestSummary(symbol,quantity);
        output = global_variables.client.futures_create_order(
            symbol   = symbol,
            side     = Client.SIDE_SELL,
            type     = Client.FUTURE_ORDER_TYPE_MARKET,
            quantity = quantity
        )
    except BinanceAPIException as e:
        print("FAIL : Order failed");
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        #printOrderResponseStatus(output);
        #printOrderResponseDetails(output);
        return output;
    finally:
        logging.info("Log : sellMarketOrder() execution completed");


def closeBuyOrders(symbol):
    try:
        x = global_variables.client.futures_get_open_orders(symbol=symbol);
    except NameError as e:
        logging.error("NameError : %s",e);
    except BinanceAPIException as e:
        print("FAIL : Failed to close buy orders")
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        df = pd.DataFrame(x);
        if(not df.empty):
            df = df[df['side']=="BUY"];
            for index in df.index:
                global_variables.client.futures_cancel_order(symbol=symbol,orderId=df["orderId"][index]);
    finally:
        logging.info("Log : closeBuyOrders() execution completed");
        

def closeSellOrders(symbol):
    try:
        x = global_variables.client.futures_get_open_orders(symbol=symbol);
    except NameError as e:
        logging.error("NameError : %s",e);
    except BinanceAPIException as e:
        print("FAIL : Failed to close sell orders");
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        df = pd.DataFrame(x);
        if(not df.empty):
            df = df[df['side']=="SELL"];
            for index in df.index:
                global_variables.client.futures_cancel_order(symbol=symbol,orderId=df["orderId"][index]);
    finally:
        logging.info("Log : closeSellOrders() execution completed");

########################################################################################


################################# Order status related functions #######################

def printOrderRequestSummary(symbol,volume,price=0):
    logging.info("Order requested for : ");
    logging.info("symbol=%s",symbol);
    logging.info("volume=%f",volume);
    logging.info("price=%f",price);


def printOrderResponseStatus(order):
    try:
        if "orderId" not in order:
            print("Order not created");
        else:
            status = order.get("status");
            if status == "FILLED":
                print("SUCCESS : Order filled successfully");
            elif status in ["NEW","PARTIALLY_FILLED"]:
                print("order placed but not filled yet");
            else:
                print("Order Status: %s", status);
    except (UnboundLocalError, TypeError) as e:
        print("FAIL : Order not created. Order response status empty");
        logging.error("Order place function not executed correctly");
    finally:
        logging.info("Log : printOrderResponseStatus() execution completed");    
            
    
def printOrderResponseDetails(order):
    try:
        df = pd.DataFrame([order]);
        df = df[["orderId","status","executedQty","avgPrice"]];
    except (UnboundLocalError, KeyError) as e:
        print("FAIL : Order response details empty");
        logging.error("Order place function not executed correctly");
    else:
        print(df.to_string());
    finally:
        logging.info("Log : printOrderResponseDetails() execution completed");    
        
   
def printAssetBalance():
    asset_bal = getAssetBalance();
    print(asset_bal);
########################################################################################


############################### Profilt/Loss realted functions##########################

def getProfit(symbol):
    try:
        x = global_variables.client.futures_position_information(symbol=symbol);
    except BinanceAPIException as e:
        logging.error("Status:%s",e.status_code);
        logging.error("Error code:%s",e.code);
        logging.error("Message:%s",e.message);
    else:
        df = pd.DataFrame(x);
        total_profit = 0;
        curr_price = getCurrentPrice(symbol);
        for index in df.index:
            total_profit += (curr_price - float(df["entryPrice"][index])) * float(df["positionAmt"][index]);
        return total_profit;
    finally:
        logging.info("Log : getProfit() execution completed");

########################################################################################

