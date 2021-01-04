import os
import asyncio

from openapi_client.openapi_streaming import run_stream_consumer
from openapi_client.openapi_streaming import print_event

token = os.getenv('TINVEST_SANDBOX_TOKEN', '')


candle_subs = [{'figi': 'BBG0018SLDN0', 'interval': '1min'}]
orderbook_subs = [{'figi': 'BBG0018SLDN0', 'depth': 1}]
instrument_info_subs = [{'figi': 'BBG0018SLDN0'}]

run_stream_consumer(token, candle_subs, orderbook_subs, instrument_info_subs, 
on_candle_event=print_event, 
on_orderbook_event=print_event,
on_instrument_info_event=print_event)

