from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

animals = ['Кошка', 'Собака']


class RequestFood(StatesGroup):
    waiting_for_pet_choice = State()
    waiting_for_pet_weight = State()


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in animals:
        keyboard.add(name)
    await message.answer("Выберите своего питомца:", reply_markup=keyboard)
    await state.set_state(RequestFood.waiting_for_pet_choice.state)