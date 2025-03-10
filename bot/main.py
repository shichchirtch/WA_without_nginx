import threading
import asyncio
import uvicorn
from my_fast_api import f_api  # <-- Импортируем FastAPI приложение
from bot_instance import bot, bot_storage_key, dp
from command_handlers import ch_router

def run_fastapi():
    uvicorn.run(f_api, host="0.0.0.0", port=8000, reload=False)  # Запуск FastAPI

async def main():
    # await dp.storage.set_data(key=bot_storage_key, data={})
    # await set_main_menu(bot)
    dp.include_router(ch_router)
    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    # Запускаем FastAPI в отдельном потоке
    f_api_thread = threading.Thread(target=run_fastapi, daemon=True)
    f_api_thread.start()

    # Запускаем асинхронного бота
    asyncio.run(main())  # <-- Здесь должен стартовать бот




#
# import uvicorn
# from command_handlers import ch_router
# # from start_menu import set_main_menu
# from bot_instance import bot, bot_storage_key, dp
# from my_fast_api import f_api
# import threading, asyncio
#
#
# def run_fastapi():
#     uvicorn.run(f_api, host="0.0.0.0", port=8000, reload=False)  # <-- Запускаем FastAPI
#
#
# async def main():
#     # await dp.storage.set_data(key=bot_storage_key, data={})
#     # await set_main_menu(bot)
#     dp.include_router(ch_router)
#     # Запускаем бота
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, skip_updates=True)
#
# if __name__ == "__main__":
#     f_api_thread = threading.Thread(target=run_fastapi, daemon=True)
#     f_api_thread.start()
#
#     # Запускаем асинхронного бота
#     asyncio.run(main())
#
#
