import asyncio
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from pgdb import create_db_connection, insert_data_user, get_product, get_categories, get_size
from setting import bot

animals = asyncio.run(get_categories())
weight = asyncio.run(get_size())


class RequestFood(StatesGroup):
    animal = State()
    size = State()


async def start_handler(message: types.Message):
    # Вносим данные о пользователе в бд
    conn = await create_db_connection()

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    registration_date = datetime.now()

    await insert_data_user(conn, user_id, username, first_name, last_name, registration_date)
    await conn.close()

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = "Выбрать корм"
    keyboard.add(button)
    await message.reply("""Здравствуйте! Здесь вы найдете лучший корм для вашего любимца!)\n 
Если у вас есть вопросы или предложения - напишите нашему менеджеру!\nКонтакты: @the_ugolkov""", reply_markup=keyboard)


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*animals)
    await message.answer("Какой у вас питомец?", reply_markup=keyboard)
    # Обновляем состояние
    await state.set_state(RequestFood.animal.state)


async def size_chosen(message: types.Message, state: FSMContext):
    if message.text.capitalize() not in animals:
        await message.answer("Пожалуйста, выберите питомца, используя клавиатуру ниже.")
        return
    # Обновляем словарь данных состояния
    await state.update_data(animal=message.text.capitalize())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*weight)

    await message.answer("Выберите нужный вес пачки корма (в килограммах)", reply_markup=keyboard)
    # Обновляем состояние
    await state.set_state(RequestFood.size.state)


async def product_output(message: types.Message, state: FSMContext):
    if message.text not in weight:
        await message.answer("Пожалуйста, выберите вес упаковки, используя клавиатуру ниже.")
        return

    data = await state.get_data()
    size = message.text
    chat_id = message.chat.id

    # Получаем список доступных товаров по разпросу
    conn = await create_db_connection()
    products = await get_product(conn, data['animal'], size)
    await conn.close()

    # Проверка наличия результатов по запросу
    if not len(products):
        await message.answer("К сожалению, на данный момент по вашему запросу нет достуных вариантов.")
    elif len(products):
        await message.answer("Вот что у нас есть для вас:")

        for product in products:
            product_name = product['product_name']
            size = product['weight']
            price = product['price']
            image_url = product['image_url']

            message_text = f"{product_name}\nВес: {size} кг.\nЦена: {price}₽"

            await bot.send_photo(chat_id, photo=image_url, caption=message_text)
    # Поставка состояния в исходное положение
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start", state="*")
    dp.register_message_handler(food_start, regexp="Выбрать корм", state="*")
    dp.register_message_handler(food_start, commands="food", state="*")
    dp.register_message_handler(size_chosen, state=RequestFood.animal)
    dp.register_message_handler(product_output, state=RequestFood.size)
