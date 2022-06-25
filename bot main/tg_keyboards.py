from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup



main_keyboard = ReplyKeyboardMarkup(row_width=2, 
                                    keyboard=[
                                [
                                    KeyboardButton(
                                        text="🤝P2P",
                                        callback_data="p2p"
                                    )
                                ]    
                              ],
                              resize_keyboard=True,
                              )



                              
p2p_main_buttons = [
    InlineKeyboardButton(text=f"💷Fiat", callback_data="fiat_p2p"),
    InlineKeyboardButton(text=f"💵Asset", callback_data="asset_p2p"),
    InlineKeyboardButton(text=f"💳Bank", callback_data="paytype_p2p"),
    InlineKeyboardButton(text=f"💰Limit", callback_data="limit_p2p"),
    InlineKeyboardButton(text=f"🔢Count", callback_data="count_p2p"),
    InlineKeyboardButton(text=f"⏰Time Limit", callback_data="time_limit_p2p"),
    InlineKeyboardButton(text="⭕️Завершить", callback_data="cancel_p2p"),
    InlineKeyboardButton(text="✅Запустить", callback_data="submit_p2p"),
    
]

p2p_change = InlineKeyboardMarkup(row_width=2).add(*p2p_main_buttons)



p2p_assets_buttons = [
    InlineKeyboardButton(text="USDT", callback_data="USDT"),
    InlineKeyboardButton(text="BTC", callback_data="BTC"),
    InlineKeyboardButton(text="BUSD", callback_data="BUSD"),
    InlineKeyboardButton(text="BNB", callback_data="BNB"),
    InlineKeyboardButton(text="ETH", callback_data="ETH"),
    InlineKeyboardButton(text="RUB", callback_data="RUB"),
    InlineKeyboardButton(text="SHIB", callback_data="SHIB"),
]

p2p_assets_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True).add(*p2p_assets_buttons)


p2p_fiat_buttons = [
    InlineKeyboardButton(text="RUB", callback_data="RUB"),
    InlineKeyboardButton(text="USD", callback_data="USD"),
    InlineKeyboardButton(text="EUR", callback_data="EUR"),
    InlineKeyboardButton(text="GBP", callback_data="GBP"),

]

p2p_fiat_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(*p2p_fiat_buttons)

p2p_paytype_buttons = [
    InlineKeyboardButton(text="Тинькофф", callback_data="Tinkoff"),
    InlineKeyboardButton(text="Росбанк", callback_data="RosBank"),
    InlineKeyboardButton(text="QIWI", callback_data="QIWI"),
    InlineKeyboardButton(text="YandexMoney", callback_data="YandexMoney"),

]

p2p_paytype_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(*p2p_paytype_buttons)