import logging
import bot.logging_config
from datetime import datetime, timezone
import threading
import time
import subprocess
import ctypes
import sys
import os

from bot import cli_func
from bot import client_wrapper
from bot import orders
from bot import global_variables

# from bot import(
    # runCLI,
    # createClient,
    # printOrderResponseStatus,
    # printOrderResponseDetails,
    # printAssetBalance,
    # stop_flag,
    # start_bot,
    # client,
    # api_key,
    # api_secret,
    # testnet_url,
    # option,
    # placeOrder,
    # checkQuantity,
    # checkPriceLimit,
    # checkEnvVariables,
# )



def initBOT():
    client_wrapper.getEnvVariables();
    client_wrapper.createClient(global_variables.api_key, global_variables.api_secret, global_variables.testnet_url, True);
   
                    
def startBOT():
    logging.info("LOG : BOT running");
    if(global_variables.option == 1):
        order_status = orders.placeOrder();
        client_wrapper.printOrderResponseStatus(order_status);
        client_wrapper.printOrderResponseDetails(order_status);
    
    if(global_variables.option ==2):
         client_wrapper.printAssetBalance();
    
    logging.info("Log : BOT stopped");
              

def getTimeDiff():
    servertime = global_variables.client.get_server_time();
    system_time_utc = datetime.now(timezone.utc);
    
    server_time_ms = servertime['serverTime'];
    server_time_sec = server_time_ms/1000;
    server_time_utc = datetime.fromtimestamp(server_time_sec, tz=timezone.utc);
    #print("Binance server time (UTC): ", server_time_utc.strftime("%Y-%m-%d %H:%M:%S"));
    #print("System time (UTC): ", system_time_utc.strftime("%Y-%m-%d %H:%M:%S"));
    
    system_time_sec = system_time_utc.timestamp();
    
    #print("Server time in seconds since linux epoch = ",server_time_sec);
    #print("system time in seconds since linux epoch = ",system_time_sec);
    
    time_diff = server_time_sec - system_time_sec;
    
    #print("Diffrence in time = ", time_diff); 
    global_variables.client.timestamp_offset = time_diff;
    

#################### OS time sync and admin mode script run mechanism ##################

def runAsAdmin():
    try:
        is_admin = ctypes.windll.shell32.IsUserAdmin();
    except:
        is_admin = False;
        
    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1);
        sys.exit();
        
        
def syncWindowsTime():
    try:
        subprocess.run(["powershell","-Command","Start-Process w32tm -ArgumentList '/resync' -Verb Runas"], check=True);
        print("Time synced successfully");
    except Exception as e:
        print("Time syns failed:",e);

########################################################################################

################################### Run BOT ############################################
def taskTime():
    while not global_variables.stop_flag:
        getTimeDiff();
        
        
def taskBOT():    
    startBOT();    
    global_variables.stop_flag = True;
        

def main():
    #runAsAdmin();
    syncWindowsTime();
    cli_func.runCLI();
    initBOT(); ##BOT Initialization
    
    t1 = threading.Thread(target=taskTime);
    t2 = threading.Thread(target=taskBOT);

    t1.start();
    t2.start();

    t1.join();
    t2.join();
    
if __name__ == "__main__":
    main();

########################################################################################

