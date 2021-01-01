import os
import asyncio

from openapi_client.openapi_streaming import run_stream_consumer
from openapi_client.openapi_streaming import print_event



"""async def main() -> None:
    async with ti.Streaming(config.TOKEN) as streaming:
        await streaming.candle.subscribe('BBG0013HGFT4', ti.CandleResolution.min1)
        await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
        await streaming.instrument_info.subscribe('BBG0013HGFT4')
        async for event in streaming:
            print(event)  # noqa:T001


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass"""


token = os.getenv('TINVEST_SANDBOX_TOKEN', '')

candle_subs = [{'figi': 'BBG000B9XRY4', 'interval': '1min'},
               {'figi': 'BBG009S39JX6', 'interval': '1min'}]
orderbook_subs = [{'figi': 'BBG0013HGFT4', 'depth': 1},
                  {'figi': 'BBG009S39JX6', 'depth': 3}]
instrument_info_subs = [{'figi': 'BBG000B9XRY4'}, {'figi': 'BBG009S39JX6'}]

run_stream_consumer(token,
                    candle_subs, orderbook_subs, instrument_info_subs,
                    on_candle_event=print_event,
                    on_orderbook_event=print_event,
                    on_instrument_info_event=print_event)
