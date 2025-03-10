from aiogram import Router, html
import asyncio
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from python_db  import users_db, user_dict
from bot_instance import bot_storage_key, dp, FSM_ST
from postgress_functions import check_user_in_table, insert_new_user_in_table
from python_db import users_db

ch_router = Router()

@ch_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    # if not await check_user_in_table(user_id):
    print(message.from_user.id)

        # await state.set_state(FSM_ST.after_start)
        # await insert_new_user_in_table(user_id, user_name)
        # bot_dict = await dp.storage.get_data(key=bot_storage_key)  # Получаю словарь бота
        # bot_dict[message.from_user.id] = {'name':user_name, 'order':{}}  # Создаю пустой словарь для заметок юзера
    users_db[user_id] = user_dict
        # await dp.storage.update_data(key=bot_storage_key, data=bot_dict)  # Обновляю словарь бота

    await message.answer(text=f'{html.bold(html.quote(user_name))}, '
                              f'Hallo !\nI am MINI APP Bot'
                              f'🎲',
                         parse_mode=ParseMode.HTML)
    await message.answer("Нажми на кнопку, чтобы открыть приложение!")
    # else:
    #     print('start else works')
    #     await insert_new_user_in_table(user_id, user_name)
    #     att = await message.answer(text='Bot was restated on server')
    #     await message.delete()
    #     await asyncio.sleep(2.5)
    #     await att.delete()


@ch_router.message(Command('help'))
async def help_command(message: Message):
    user_id = message.from_user.id
    temp_data = users_db[user_id]['bot_answer']
    if temp_data:
        await temp_data.delete()
    att = await message.answer('help')
    users_db[user_id]['bot_answer'] = att
    await asyncio.sleep(2)
    await message.delete()


@ch_router.message()
async def trasher(message: Message):
    print('TRASHER')
    await asyncio.sleep(1)
    await message.delete()