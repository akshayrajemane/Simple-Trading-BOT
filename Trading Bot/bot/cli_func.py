from . import global_variables


def runCLI():
    print("");
    print("Welcome to Binance Futures Testnet trading...");
    print("");
    print("");
    
    while True:
        print("Choose one option");
        print("1. Place order");
        print("2. Check asset balance"); # TODO:refine later
        #TODO: Add few more options
        print("0. Exit");

        global_variables.option = int(input("Enter any one of the above option numebr : "));
        if(global_variables.option not in range(0,10)):
            print("Type valid input : 0-9");
            continue;
        elif(global_variables.option == 0):
            return 0;
        else:
            break;
    
    
    if(global_variables.option == 1):
        while True:
            global_variables.symbol = input("Enter symbol (in CAPS) e.g. BTCUSDT : ");
            if(global_variables.symbol not in global_variables.symbols):  #add few more symbols
                print("Enter valid symbol : BTCUSDT/BNBUSDT");
                continue;
            else:
                break;
    
    
        while True:
            global_variables.side = input("Choose side (BUY/SELL) : ");
            if(global_variables.side not in ("BUY","SELL")):
                print("Type valid input : BUY/SELL");
                continue;
            else:
                break;
        
        
        while True:
            global_variables.order_type = input("Enter order type (in CAPS) e.g. MARKET/LIMIT : ");
            if(global_variables.order_type not in ("MARKET", "LIMIT")):  #add few more symbols
                print("Enter valid order type : MARKET/LIMIT");
                continue;
            else:
                break;
            
            
        while True:
            global_variables.quantity = float(input("Enter quantity (positive number) : "));
            if(global_variables.quantity):
                break;
            else:
                print("Type valid input : positive decimal number");
                continue;
        
            
        if(global_variables.order_type == "LIMIT"):
            while True:  
                global_variables.price = float(input("Enter price for LIMIT order : "));
                if(global_variables.price <= 0): #Add function call for valid price detection
                    print("Enter a valid price (positive number) ");
                    continue;
                else:
                    break;