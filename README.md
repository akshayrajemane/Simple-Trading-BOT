# Simple-Trading-BOT
This repository contains a simple automated trading bot built using core Python and the python‑binance API. It demonstrates how to connect to Binance Testnet, fetch asset balance, place orders, and structure a clean, modular trading bot project.


Setup Steps : 
  install python-binance liberary
  pip install python-binance
  add .env file:
    -- Please create a file named .env.
    -- Add your BINANCE_API_KEY and BINANCE_API_SECRET inside it.
    -- Place the .env file in the same directory as cli.py.

How to run examples: 
  Open a terminal at the file (cli.py) location and execute the file -> python3 cli.py
  This will give CLI interface to the user. 
  User can proceed with instructions on the screen.
  Upon successfull execution, it will generate bot.log log file.

Assumptions : 
  Your system must have already installed Python3
  
Note : 
  If you encounter any python-liberary missing error. Please install respective python-liberary and run this command. -> python3 cli.py
