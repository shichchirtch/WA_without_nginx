from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from external_functions import send_telegram_message
from bot_instance import dp, bot_storage_key
import datetime
import pytz
from python_db import users_db
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


f_api = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Разрешить все источники (можно ограничить)
            allow_credentials=True,
            allow_methods=["*"],  # Разрешить все методы (POST, GET, OPTIONS и т.д.)
            allow_headers=["*"],  # Разрешить все заголовки
        )
    ]
)


static_dir = Path(__file__).parent / "static"  # Теперь путь точный
templ_dir = Path(__file__).parent / "templates"
f_api.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templ_dir)

pizzas = [
    {"id": 1, "name": "Margorita", "image": "margherita.png",
     "description": "Томатный соус, моцарелла, базилик.",
     'price': 15},
    {"id": 2, "name": "Pepperoni", "image": "pepperoni.png",
     "description": "Томатный соус, моцарелла, пепперони.",
     'price': 16},
    {"id": 3, "name": "Four Cheese", "image": "four_cheese.png",
     "description": "Моцарелла, пармезан, горгонзола, эмменталь.", 'price': 17},
    {"id": 4, "name": "Hawaii", "image": "hawaiian.png",
     "description": "Томатный соус, моцарелла, ананасы, ветчина.", 'price': 18}
]
server_cart = []


@f_api.post("/receive_telegram_data")
async def receive_telegram_data(data: dict):
    print("📦 Полученные данные от Telegram:", data)
    return {"success": True, "received_data": data}


@f_api.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "pizzas": pizzas})


@f_api.get("/pizza/{pizza_id}")
async def pizza_detail(request: Request, pizza_id: int):
    pizza = next((p for p in pizzas if p["id"] == pizza_id), None)
    if not pizza:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    return templates.TemplateResponse("pizza.html", {"request": request, "pizza": pizza})


@f_api.post("/cart")
async def cart_page(data: dict):
    user_name = data.get('name')
    user_id = data.get('user_id')
    address = data.get("address")
    phone = data.get("phone")
    payment = data.get("payment")
    order = data.get("order", [])

    if not address or not phone:
        raise HTTPException(status_code=400, detail="Заполните все поля!")

    message = f"🛒 *Заказ оформлен!*\n👤 *Заказчик:* {user_name}\n📍 *Адрес:* {address}\n📞 *Телефон:* {phone}\n💳 *Оплата:* {payment}\n🍕 *Состав заказа:*\n"
    total_price = sum(item.get("price", 0) * item.get("quantity", 1) for item in order)
    order_user = f'{user_name}, {phone}'
    for item in order:
        one_stelle =  f"• {item['name']} x{item['quantity']} - {item['price'] * item['quantity']} €\n"
        message += one_stelle
        order_user += one_stelle
    message += f"\n💰 *Сумма к оплате:* {total_price} €"
    send_telegram_message(message, user_id)  # Отправляю сообщение
    print('message = ', message)
    berlin_tz = pytz.timezone("Europe/Berlin")
    a = datetime.datetime.now(berlin_tz).replace(second=0, microsecond=0)
    formatted_time = a.strftime("%H:%M %d.%m.%Y") # выставляю время
    order_user += f' Total {total_price} Data : {formatted_time}'

    # bot_dict = await dp.storage.get_data(key=bot_storage_key)
    # us_dict = bot_dict.get(user_id, {})
    # us_index = len(us_dict['order']) + 1
    # us_dict['order'][us_index] = order_user

    # await dp.storage.update_data(key=bot_storage_key, data=bot_dict)
    index = len(users_db[user_id]['orders'])+1
    users_db[user_id]['orders'][index] = order_user
    data = users_db[user_id]['orders']
    print('dats = ', data)
    server_cart.clear()
    return {"success": True}


@f_api.get("/cart")
async def get_cart(request: Request):
    total_price = sum(item['price'] for item in server_cart)
    return templates.TemplateResponse("cart.html",
    {"request": request, "cart": server_cart, "total_price": total_price})


@f_api.post("/add-to-cart")
async def add_to_cart(data: dict):
    pizza_id = data.get("pizza_id")
    quantity = data.get("quantity")
    pizza_price = data.get("price")

    pizza = next((p for p in pizzas if p["id"] == int(pizza_id)), None)
    if not pizza:
        raise HTTPException(status_code=404, detail="Пицца не найдена")

    existing_pizza = next((item for item in server_cart if item["pizza_id"] == pizza_id), None)
    if existing_pizza:
        existing_pizza["quantity"] += quantity
    else:
        server_cart.append(
            {"pizza_id": pizza_id, "name": pizza["name"], "quantity": quantity, 'price': pizza_price * quantity})

    return {"success": True}


@f_api.post("/reset-cart")
async def reset_cart():
    server_cart.clear()
    return {"success": True}





