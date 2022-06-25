
default_p2p_values = {
    'asset': "USDT", 
    'fiat': "RUB", 
    'paytype': "Tinkoff",  
    'limit': 3, 
    'time_limit': 10,
    'maxmin': 100000,
}

query_msg_p2p_choices = None
msg11 = None

async def change_default_p2p_values(name, value):
    global default_p2p_values
    default_p2p_values[name] = value
    return

async def change_msg(msg1):
    global query_msg_p2p_choices
    query_msg_p2p_choices = msg1
    return

async def change_msg11(msg1):
    global msg11 
    msg11 = msg1
    return

