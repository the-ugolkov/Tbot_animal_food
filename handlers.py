from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

animals = ['Кошка', 'Собака']
weight = [1, 3, 5, 15, 25]


class RequestFood(StatesGroup):
    waiting_for_pet_choice = State()
    waiting_for_weight = State()


async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button = "Выбрать корм"
    keyboard.add(button)
    await message.reply("""Здравствуйте! Здесь вы найдете лучший корм для вашего любимца!)\n 
Если у вас есть вопросы или предложения - напишите нашему менеджеру!\n Контакты:""", reply_markup=keyboard)


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in animals:
        keyboard.add(name)
    await message.answer("Какой у вас питомец?", reply_markup=keyboard)
    await state.set_state(RequestFood.waiting_for_pet_choice.state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands="start", state="*")
    dp.register_message_handler(food_start, regexp="Выбрать корм", state="*")
