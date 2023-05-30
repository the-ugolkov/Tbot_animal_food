from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

animals = ['Кошка', 'Собака']
weight = [1, 3, 5, 15, 25]


class RequestFood(StatesGroup):
    waiting_for_pet_choice = State()
    waiting_for_pet_weight = State()


async def food_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in animals:
        keyboard.add(name)
    await message.answer("Выберите своего питомца:", reply_markup=keyboard)
    await state.set_state(RequestFood.waiting_for_pet_choice.state)


async def food_chosen(message: types.Message, state: FSMContext):
    if message.text.capitalize() not in animals:
        await message.answer("Пожалуйста, выберите питомца, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.capitalize())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in weight:
        keyboard.add(size)
    await state.set_state(RequestFood.waiting_for_pet_weight.state)
    await message.answer("Теперь выберите размер пачки:", reply_markup=keyboard)

