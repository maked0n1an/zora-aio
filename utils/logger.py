import sys
from loguru import logger

from utils.constants import Status
   
def setup_logger_for_output():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )
    logger.add(
        "main.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )
    
    logger.level(Status.HAS_NFT, no=26, color="<green>")
    logger.level(Status.APPROVED, no=27, color="<green>")
    logger.level(Status.MINTED, no=28, color="<green>")
    logger.level(Status.BRIDGED, no=29, color="<green>")
    
    return logger

loggers = {}

def setup_logger_for_wallet(wallet_name):
    if wallet_name not in loggers:
        wallet_logger = logger.bind(wallet_name=wallet_name)       
        wallet_logger.add(
            rf"logs\log_{wallet_name}.log",
            format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
            "{level: <8}</level> | <cyan>"
            "</cyan> <white>{message}</white>",
            filter=lambda record: record["extra"].get("wallet_name") == wallet_name
        )        
        loggers[wallet_name] = wallet_logger
        return wallet_logger
    else:
        return loggers[wallet_name]
     