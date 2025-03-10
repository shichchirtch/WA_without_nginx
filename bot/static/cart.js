// Находим форму по ID и добавляем обработчик события "submit" (отправка формы)
document.getElementById("orderForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Останавливаем стандартную отправку формы, чтобы обработать данные вручную
    // Пробуем получить данные из localStorage
    const telegramData = localStorage.getItem("telegramData");
    let name = ''
    let user_id = 1
    if (telegramData) {
        const userData = JSON.parse(telegramData);
        console.log("📦 Восстановленные данные от Telegram: ", userData);
        console.log("✅ User userData.user:  ", userData.user);
        name = userData.user.first_name || "❌ user_id не найден!";
        user_id = userData.user.id
        console.log("✅ User NAME:", name);

    } else {
        console.error("❌ Данные Telegram не найдены в localStorage!");
    }
    // Получаем значения полей ввода
    const address = document.getElementById("address").value;
    const phone = document.getElementById("phone").value;
    const payment = document.getElementById("payment").value;
    // Валидация адреса:
    // 1. Он не должен состоять только из цифр (должна быть хотя бы одна буква).
    // 2. Длина должна быть минимум 10 символов.
    if (!/\D/.test(address) || address.length < 10) {
        alert("Адрес должен содержать хотя бы одну букву и быть не короче 10 символов.");
        return; // Прекращаем выполнение, если адрес не соответствует требованиям
    }
    // Валидация телефона:
    // 1. Должны быть только цифры и знак "+", никаких других символов.
    // 2. Длина номера должна быть от 12 до 14 символов.
    if (!/^\+?\d[\d\s]{11,13}$/.test(phone)) {
        alert("Телефон должен содержать только цифры и знак +, длиной от 12 до 14 символов.");
        return; // Прекращаем выполнение, если номер не соответствует требованиям
    }

    if (!name) {
        alert("Ошибка: Не удалось получить Telegram name.");
        return;
    }
    const HOST_PATH = 'https://bd82-2a00-20-45-33fc-21bd-f5a4-2a73-a1fb.ngrok-free.app'
    const cartItems = JSON.parse(localStorage.getItem("cart")) || [];  // Достаём корзину из localStorage
    console.log('cartItems = ', cartItems[0]['quantity'])

     if (cartItems.length === 0) {
        alert("Корзина пуста! Добавьте товары перед заказом.");
        return;
    }
     console.log("cartItems перед отправкой:", cartItems); // 0: {name: 'Маргарита', quantity: 1, price: 15}

    // Отправляем данные заказа на сервер с помощью fetch API
    fetch(`${HOST_PATH}/cart`, {
        method: "POST", // HTTP-метод запроса
        headers: { "Content-Type": "application/json" }, // Указываем, что отправляем JSON
        body: JSON.stringify({ name, user_id, address, phone, payment, order: cartItems}), // Преобразуем объект в JSON-строку

    })
    .then(response => response.json()) // Преобразуем ответ сервера в JSON
    .then(data => {
        if (data.success) { // Если сервер ответил, что заказ успешно создан
            alert("Заказ успешно оформлен!");
            localStorage.removeItem("cart"); // Очищаем корзину после заказа
            window.location.href = "/"; // Перенаправляем пользователя на главную страницу
        } else { // Если произошла ошибка на сервере
            alert("Ошибка: " + data.error);
        }
    })
    .catch(error => {
        alert("Ошибка сети при отправке заказа!"); // Выводим сообщение в случае сетевой ошибки
    });
});


document.getElementById("resetOrder").addEventListener("click", function(event) {
    event.preventDefault(); // Отменяем стандартный переход по ссылке

    fetch(`/reset-cart`, { method: "POST" }) // Отправляем запрос на сервер для очистки корзины
        .then(response => response.json()) // Преобразуем ответ в JSON
        .then(data => {
            if (data.success) {
                window.location.href = "/"; // Перенаправляем пользователя на главную страницу
            } else {
                alert("Ошибка при очистке корзины!");
            }
        })
        .catch(error => {
            alert("Ошибка сети при очистке корзины!");
        });
});



