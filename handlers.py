from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from pgdb import create_db_connection, insert_data_user, get_product
from setting import bot

animals = ['Кошка', 'Собака']
weight = ['1', '3', '5', '15', '25']


class RequestFood(StatesGroup):
    animal = State()
    size = State()


async def start_handler(message: types.Message):
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
Если у вас есть вопросы или предложения - напишите нашему менеджеру!\nКонтакты:""", reply_markup=keyboard)


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for animal in animals:
        keyboard.add(animal)
    await message.answer("Какой у вас питомец?", reply_markup=keyboard)
    await state.set_state(RequestFood.animal.state)


async def size_chosen(message: types.Message, state: FSMContext):
    if message.text.capitalize() not in animals:
        await message.answer("Пожалуйста, выберите питомца, используя клавиатуру ниже.")
        return
    await state.update_data(animal=message.text.capitalize())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for size in weight:
        keyboard.add(size)
    await state.set_state(RequestFood.size.state)
    await message.answer("Выберите нужный вес пачки корма (в килограммах)", reply_markup=keyboard)


async def product_output(message: types.Message, state: FSMContext):
    if message.text not in weight:
        await message.answer("Пожалуйста, выберите вес упаковки, используя клавиатуру ниже.")
        return

    data = await state.get_data()
    size = message.text
    chat_id = message.chat.id

    conn = await create_db_connection()
    products = await get_product(conn, data['animal'], size)
    await conn.close()
    for product in products:
        product_name = product['product_name']
        size = product['weight']
        price = product['price']
        image_url = product['image_url']

        message_text = f"{product_name}\nВес: {size} кг.\nЦена: {price}₽"

        await bot.send_photo(chat_id, photo=image_url, caption=message_text)

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start", state="*")
    dp.register_message_handler(food_start, regexp="Выбрать корм", state="*")
    dp.register_message_handler(food_start, commands="food", state="*")
    dp.register_message_handler(size_chosen, state=RequestFood.animal)
    dp.register_message_handler(product_output, state=RequestFood.size)
