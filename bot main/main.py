
from binance.error import ClientError
from binance.spot import Spot as Client
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv('API_KEY')
secret = os.getenv('SECRET_KEY')

client = Client(key=api_key, secret=secret, 
                base_url='https://testnet.binance.vision',
                show_limit_usage=True,)


async def get_ticker_price(symbol):
    try:
        return client.ticker_price(symbol=symbol)
    except ClientError:
        return '!'

