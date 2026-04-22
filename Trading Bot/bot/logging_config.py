import logging

logging.basicConfig(
    level    = logging.INFO,
    format   = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [ logging.FileHandler("bot.log", mode='w')] #, logging.StreamHandler()
    )
    
#logging.getLogger().setLevel(logging.DEBUG);
logging.getLogger("binance").setLevel(logging.WARNING);
logging.getLogger("binance.client").setLevel(logging.WARNING);
logging.getLogger("binance.rest").setLevel(logging.WARNING);

logging.getLogger("httpx").setLevel(logging.WARNING);
logging.getLogger("requests").setLevel(logging.WARNING);
logging.getLogger("urllib3").setLevel(logging.WARNING);
logging.getLogger("aiohttp").setLevel(logging.WARNING);

logging.getLogger("websockets").setLevel(logging.WARNING);

logging.getLogger("asyncio").setLevel(logging.WARNING);
logging.getLogger("asyncio.proactor").setLevel(logging.WARNING);
logging.getLogger("asyncio.windows_events").setLevel(logging.WARNING);
logging.getLogger("asyncio.windows_utils").setLevel(logging.WARNING);

root = logging.getLogger();
root.setLevel(logging.INFO);
for h in root.handlers:
    h.setLevel(logging.INFO);

