import asyncio
from aiogram.utils.exceptions import MessageNotModified

from aiogram import executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot_dispatcher import bot, dp, allowed_users

from parser_tg import p2p_func, set_parse_p2p_status

import tg_keyboards

from main import get_ticker_price

import temp_db as db



class P2PState(StatesGroup):
    waiting_asset_p2p_state = State()
    waiting_fiat_p2p_state = State()
    waiting_paytype_p2p_state = State()
    waiting_limit_p2p_state = State()
    waiting_time_limit_p2p_state = State()
    waiting_time_maxmin_p2p_state = State()


@dp.message_handler(Command('start'))
async def send_welcome(message: types.Message):
    if not message.from_user.id in allowed_users:
        await message.answer(message.from_user.id)
        return
    bot_msg = await message.answer('start', reply_markup=tg_keyboards.main_keyboard)
    await message.delete()
    # await bot_msg.delete()


@dp.message_handler(text='🤝P2P', user_id=allowed_users)
async def p2p_request(message: types.Message):
    await message.delete()
    await message.answer(await get_changed_p2p_text(), reply_markup=tg_keyboards.p2p_change)



async def get_changed_p2p_text():
    limit = format(db.default_p2p_values["maxmin"], ',').replace(',', ' ').replace('.', ',')
    return f'<i>Что-нибудь изменить?</i>\n\
<b>Asset:</b> {db.default_p2p_values["asset"]} <b>Fiat:</b> {db.default_p2p_values["fiat"]}\n\
<b>Bank:</b> {db.default_p2p_values["paytype"]}\n\
<b>Limit:</b> {limit}\n\
<b>Count:</b> {db.default_p2p_values["limit"]} <b>Time Limit:</b> {db.default_p2p_values["time_limit"]}'

@dp.callback_query_handler(text='submit_p2p', user_id=allowed_users)
async def submit_p2p(query: types.CallbackQuery):
    await query.message.delete()
    await set_parse_p2p_status(arg='on')
    msg222 = await bot.send_message(query.message.chat.id, text='P2P сессия запущена✅')
    await p2p_func(chat_id=query.message.chat.id, p2p_values=db.default_p2p_values)
    await asyncio.sleep(5)
    await msg222.delete()


@dp.callback_query_handler(text='cancel_p2p', user_id=allowed_users)
async def cancel_p2p(query: types.CallbackQuery):
    await query.message.delete()
    await set_parse_p2p_status(arg='off')
    msg = await bot.send_message(query.message.chat.id, text='P2P сессия завершена⭕️')
    print('------P2P session is over------')
    await asyncio.sleep(5)
    await msg.delete()


@dp.callback_query_handler(text='asset_p2p', user_id=allowed_users)
async def change_p2p_values_1(query: types.CallbackQuery):
    await change_p2p_values(query=query, name='asset')

@dp.callback_query_handler(text='fiat_p2p', user_id=allowed_users)
async def change_p2p_values_2(query: types.CallbackQuery):
    await change_p2p_values(query=query, name='fiat')

@dp.callback_query_handler(text='paytype_p2p', user_id=allowed_users)
async def change_p2p_values_3(query: types.CallbackQuery):
    await change_p2p_values(query=query, name='paytype')

@dp.callback_query_handler(text='count_p2p', user_id=allowed_users)
async def change_p2p_values_4(query: types.CallbackQuery):
    await change_p2p_values_manual(query=query, name='limit')

@dp.callback_query_handler(text='time_limit_p2p', user_id=allowed_users)
async def change_p2p_values_5(query: types.CallbackQuery):
    await change_p2p_values_manual(query=query, name='time_limit')

@dp.callback_query_handler(text='limit_p2p', user_id=allowed_users)
async def change_p2p_values_6(query: types.CallbackQuery):
    await change_p2p_values_manual(query=query, name='maxmin')


async def change_p2p_values(query, name):
    
    await db.change_msg(query.message.message_id)

    if name == 'asset':
        reply_markup_set = tg_keyboards.p2p_assets_keyboard

        state_set = P2PState.waiting_asset_p2p_state
        await state_set.set()
    elif name == 'fiat':
        reply_markup_set = tg_keyboards.p2p_fiat_keyboard

        state_set = P2PState.waiting_fiat_p2p_state
        await state_set.set()
    elif name == 'paytype':
        reply_markup_set = tg_keyboards.p2p_paytype_keyboard

        state_set = P2PState.waiting_paytype_p2p_state
        await state_set.set()


    msg11 = await bot.send_message(query.message.chat.id, text='Введите нужный вариант...', reply_markup=reply_markup_set)

    @dp.callback_query_handler(state=state_set)
    async def state_asset_p2p(query: types.CallbackQuery, state: FSMContext):
        
        if name == 'asset':
            if query.data not in ['USDT', 'BTC', 'BUSD', 'BNB', 'ETH', 'RUB', 'SHIB']:
                await state.finish()
                return
        if name == 'fiat':
            if query.data not in ['RUB', 'USD', 'EUR', 'GBP']:
                await state.finish()
                return
        if name == 'paytype':
            if query.data not in ['Tinkoff', 'RosBank', 'QIWI', 'YandexMoney']:
                await state.finish()
                return

        await query.message.delete()

        await state.update_data(chosen_method=query.data)
        result = await state.get_data()
        await db.change_default_p2p_values(name, result.get('chosen_method'))
        # await state.finish()
        await state.finish()

        msg = await query.message.answer(f"✅Выбор {query.data} успешно подключён.")


        try:
            await bot.edit_message_text(text=await get_changed_p2p_text(), chat_id=query.message.chat.id, message_id=db.query_msg_p2p_choices, reply_markup=tg_keyboards.p2p_change)
        except MessageNotModified:
            pass 

        
        await asyncio.sleep(5)
        await msg.delete()


    await asyncio.sleep(10)
    try:
        await msg11.delete()
        await dp.current_state().finish()
    except Exception as err:
        pass


async def change_p2p_values_manual(query, name):

    await db.change_msg(query.message.message_id)

    if name == 'limit':
        add_msg = '(От 1 до 10)'
        state_set = P2PState.waiting_limit_p2p_state
        await state_set.set()
    if name == 'time_limit':
        add_msg = '(От 2 до 1800)'
        state_set = P2PState.waiting_time_limit_p2p_state
        await state_set.set()
    if name == 'maxmin':
        add_msg = 'Сумма сделки.'
        state_set = P2PState.waiting_time_maxmin_p2p_state
        await state_set.set()



    msg11 = await bot.send_message(query.message.chat.id, text=f'Введите нужный вариант...{add_msg}')
    await db.change_msg11(msg11.message_id)

    @dp.message_handler(state=state_set)
    async def state_smth_p2p(message: types.Message, state: FSMContext):
        try:
            message_text = int(message.text)
        except ValueError:
            await state.finish()
            return
        if name == 'limit':
            if message_text > 10 or message_text < 1:
                await state.finish()
                return
        elif name == 'time_limit':
            if message_text > 1800 or message_text < 2:
                await state.finish()
                return
        elif name == 'maxmin':
            pass

        else:
            await state.finish()
            return


        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=db.msg11)

        await state.update_data(chosen_method=message_text)
        result = await state.get_data()
        await db.change_default_p2p_values(name, result.get('chosen_method'))
        # await state.finish()
        await state.finish()

        msg = await query.message.answer(f"✅Выбор {message_text} успешно подключён.")

        # await db.test_query.message.edit_text('test', reply_markup=p2p_change)
        try:
            await bot.edit_message_text(text=await get_changed_p2p_text(), chat_id=query.message.chat.id, message_id=db.query_msg_p2p_choices, reply_markup=tg_keyboards.p2p_change)
        except MessageNotModified:
            pass 

        await asyncio.sleep(5)
        await msg.delete()


    await asyncio.sleep(10)
    try:
        await msg11.delete()
        await dp.current_state().finish()
    except Exception as err:
        pass




# @dp.message_handler()
# async def send_welcome(message: types.Message):
#     # await message.answer(message.text)
#     if message.text.startswith('/'):
#         await message.delete()
#         text = message.text.upper()
#         msg = await get_ticker_price(text[1:])

#         if msg == '!':
#             answ = await message.answer('Валютная пара не найдена')
#             await asyncio.sleep(5)
#             await answ.delete()
#         else:
#             symbol = msg.get('data')['symbol']
#             price = msg.get('data')['price']
#             answ = await message.answer(f'{symbol} - {price}')
#             await asyncio.sleep(5)
#             await answ.delete()







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)