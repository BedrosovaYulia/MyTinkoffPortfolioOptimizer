import os
from openapi_client import openapi
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import numpy as np


token = os.getenv('TINVEST_TOKEN', '')
client = openapi.api_client(token)

def print_30d_operations():
    now = datetime.now(tz=timezone('Europe/Moscow'))
    yesterday = now - timedelta(days=30)
    ops = client.operations.operations_get(_from=yesterday.isoformat(), to=now.isoformat())
    return ops
    

operations=print_30d_operations()

#print(operations)
byfigi=dict()
for operation in operations.payload.operations:
    if operation.status == 'Done':
        byfigi[operation.figi] = {"summ": 0, "currency": operation.currency}

for operation in operations.payload.operations:
    if operation.status == 'Done':
        byfigi[operation.figi]["summ"] = byfigi[operation.figi]["summ"] + operation.payment
        
        
#print(operation.date, operation.figi, operation.payment, operation.currency, operation.operation_type)

pddf = pd.DataFrame(byfigi)

print(pddf)
